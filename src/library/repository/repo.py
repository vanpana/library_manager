import copy
from operator import itemgetter
from datetime import date
from library.domain.validators import LibraryException, LibraryValidatorException


class RepositoryException(LibraryException):
    pass

class DuplicateIdException(RepositoryException):
    pass

class InexistentIdException(RepositoryException):
    pass

class BookRepository(object):
    '''
    Bridge between UI and main book operations.
    '''

    def __init__(self, validator_class):
        self.__validator_class = validator_class
        self.__book_entities = []
        self.__book_backup = []
        self.__book_backup_redo = []

    def backup_op(self):
        self.__book_backup.append(copy.deepcopy(self.__book_entities))

    def undo_op(self):
        if len(self.__book_backup) > 0:
            self.__book_backup_redo.append(copy.deepcopy(self.__book_entities))
            self.__book_entities = copy.deepcopy(self.__book_backup[len(self.__book_backup) - 1])
            self.__book_backup.pop(len(self.__book_backup)-1)
        else:
            raise ValueError("No previous actions")

    def redo_op(self):
        if len(self.__book_backup) > 0:
            self.__book_backup.append(copy.deepcopy(self.__book_entities))
            self.__book_entities = copy.deepcopy(self.__book_backup_redo[len(self.__book_backup_redo) - 1])
            self.__book_backup_redo.pop(len(self.__book_backup_redo)-1)
        else:
            raise ValueError("No previous undo")

    def exit_update_data(self):
        pass

    def get_all(self):
        return self.__book_entities

    def __getitem__(self, key):
        for book in self.__book_entities:
            if book.book_id == key:
                return book
        return None

    def __setitem__(self, key, item):
        try:
            self.__validator_class.validate_book(item)
        except LibraryValidatorException as pve:
            raise LibraryException(pve)

        self.__book_backup_redo = []
        if self[key] != None:
            for book in range(0, len(self.__book_entities)):
                if self.__book_entities[book].book_id == key:
                    self.__book_entities[book] = item
        else:
            self.__book_entities.append(item)


    def __delitem__(self, key):
        self.__book_backup_redo = []
        if self[key] is None:
            raise InexistentIdException("No book with id {0}.".format(key))
        for book in range(0, len(self.__book_entities)):
            if self.__book_entities[book].book_id == key:
                self.__book_entities.pop(book)
                break
        ###TO DO DELETE RENTALS

    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self):
        if (self.counter < len(self.__book_entities)):
            self.counter = self.counter + 1
            return self.__book_entities[self.counter - 1]
        raise StopIteration


class ClientRepository(object):
    '''
    Bridge between UI and main client operations.
    '''

    def __init__(self, validator_class):
        self.__validator_class = validator_class
        self.__client_entities = []
        self.__client_backup = []
        self.__client_backup_redo = []

    def backup_op(self):
        self.__client_backup.append(copy.deepcopy(self.__client_entities))

    def undo_op(self):
        if len(self.__client_backup) > 0:
            self.__client_backup_redo.append(copy.deepcopy(self.__client_entities))
            self.__client_entities = copy.deepcopy(self.__client_backup[len(self.__client_backup) - 1])
            self.__client_backup.pop(len(self.__client_backup)-1)
        else:
            raise ValueError("No previous actions")

    def redo_op(self):
        if len(self.__client_backup) > 0:
            self.__client_backup.append(copy.deepcopy(self.__client_entities))
            self.__client_entities = copy.deepcopy(self.__client_backup_redo[len(self.__client_backup_redo) - 1])
            self.__client_backup_redo.pop(len(self.__client_backup_redo)-1)
        else:
            raise ValueError("No previous actions")

    def exit_update_data(self):
        pass

    def get_all(self):
        return self.__client_entities

    def __getitem__(self, key):
        for client in self.__client_entities:
            if client.client_id == key:
                return client
        return None

    def __setitem__(self, key, item):
        try:
            self.__validator_class.validate_client(item)
        except LibraryValidatorException as pve:
            raise LibraryException(pve)
        self.__client_backup_redo = []
        if self[key] != None:
            for client in range(0, len(self.__client_entities)):
                if self.__client_entities[client].client_id == key:
                    self.__client_entities[client] = item
        else:
            self.__client_entities.append(item)


    def __delitem__(self, key):
        self.__client_backup_redo = []
        if self[key] is None:
            raise InexistentIdException("No client with id {0}.".format(key))
        for client in range(0, len(self.__client_entities)):
            if self.__client_entities[client].client_id == key:
                self.__client_entities.pop(client)
                break

    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self):
        if (self.counter < len(self.__client_entities)):
            self.counter = self.counter + 1
            return self.__client_entities[self.counter - 1]
        raise StopIteration


class RentalRepository(object):
    '''
    Bridge between UI and main rental operations.
    '''

    def __init__(self, validator_class):
        self.__validator_class = validator_class
        self.__rental_entities = {}
        self.__rental_backup = []
        self.__rental_backup_redo = []

    def find_by_id(self, rental_id):
        if rental_id in self.__rental_entities:
            return self.__rental_entities[rental_id]
        return None

    def rent(self, rental):
        if rental.book_id == -1:
            raise InexistentIdException("No book with id {0}".format(rental.book_id))
        for r in self.__rental_entities:
            if self.__rental_entities[r].book_id == rental.book_id and type(self.__rental_entities[r].returned) == str:
                raise DuplicateIdException("Book with id {0} is already rented until {1}!" \
                                       .format(rental.book_id, rental.due))

        if rental.client_id == -1:
            raise InexistentIdException("No client with id {0}".format(rental.client_id))

        if not self.find_by_id(rental.rental_id) == None:
            raise DuplicateIdException("Rental already existing with with id {0}".format(rental.rental_id))

        ##########CHECK BOOK AND CLIENT
        self.__validator_class.validate_rental(rental)
        self.__rental_entities[rental.rental_id] = rental

    def return_rental(self, rental_id, returned):
        rental = self.find_by_id(rental_id)
        if rental == None:
            raise InexistentIdException("No rental with with id {0}".format(rental_id))
        if rental.rented > returned:
            raise DuplicateIdException("Returned date is before rental day!")
        rental.returned = returned

    def backup_op(self):
        self.__rental_backup.append(copy.deepcopy(self.__rental_entities))

    def undo_op(self):
        if len(self.__rental_backup) > 0:
            self.__rental_backup_redo.append(copy.deepcopy(self.__rental_entities))
            self.__rental_entities = copy.deepcopy(self.__rental_backup[len(self.__rental_backup) - 1])
            self.__rental_backup.pop(len(self.__rental_backup)-1)
        else:
            raise ValueError("No previous actions")

    def redo_op(self):
        if len(self.__rental_backup) > 0:
            self.__rental_backup.append(copy.deepcopy(self.__rental_entities))
            self.__rental_entities = copy.deepcopy(self.__rental_backup_redo[len(self.__rental_backup_redo) - 1])
            self.__rental_backup_redo.pop(len(self.__rental_backup_redo)-1)
        else:
            raise ValueError("No previous actions")

    def exit_update_data(self):
        pass

    def get_all(self):
        return self.__rental_entities.values()
