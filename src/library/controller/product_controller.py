from operator import itemgetter

from library.domain.entities import Book, Client, Rental
from datetime import date

from library.domain.validators import LibraryException


class RepositoryException(LibraryException):
    pass

class DuplicateIdException(RepositoryException):
    pass

class InexistentIdException(RepositoryException):
    pass

class BookController(object):
    '''
    The bridge between the UI module and the Book Repository.
    '''
    def __init__(self, book_repository):
        self.__book_repository = book_repository

    def add_book(self, book_id, title, description, author):
        if self.__book_repository[book_id] == None:
            self.backup_op()
            book = Book(book_id, title, description, author)
            self.__book_repository[book_id] = book
        else:
            raise DuplicateIdException("duplicate id {0}.".format(book_id))

    def delete_book(self, book_id):
        self.backup_op()
        del self.__book_repository[book_id]
        # TODO if book gets deleted, do something with the rental

    def update_book(self, book_id, title, description, author):
        self.backup_op()
        book = Book(book_id, title, description, author)
        if self.__book_repository[book_id] is None:
            raise InexistentIdException("No book with id {0}.".format(book_id))
        if title != "":
            book.title = title
        if description != "":
            book.description = description
        if author != "":
            book.author = author
        self.__book_repository[book_id] = book

    def find_by_id(self, book_id):
        return self.__book_repository[book_id]
    
    def find_book(self, book_type, book_field): #type: 1 - by title, 2 - by description, 3 - by author
        book_list = list(self.__book_repository.get_all())
        list_for_print = []
        for b in book_list:
            if book_type == 1 and book_field.replace(" ", "").lower() \
                    in b.title.replace(" ",
                                                                                                               "").lower():
                list_for_print.append(b)
            if book_type == 2 and book_field.replace(" ", "").lower() in self.__book_repository.get_all()[b].description.replace(
                    " ", "").lower():
                list_for_print.append(self.__book_repository.get_all()[b])
            if book_type == 3 and book_field.replace(" ", "").lower() in self.__book_repository.get_all()[b].author.replace(" ",
                                                                                                                "").lower():
                list_for_print.append(self.__book_repository.get_all()[b])
        return list_for_print
    
    def sort_by_rents(self):
        sortedv = []
        for b in list(self.get_all()):
            sortedv.append({"id": b.book_id, "times_rented": b.times_rented})
        sortedv = sorted(sortedv, key= \
            itemgetter("times_rented"), reverse=True)
        list_for_return = []
        for b in range(0, len(sortedv)):
            list_for_return.append(self.find_by_id(sortedv[b]["id"]))
        return list_for_return

    def sort_by_days(self):
        sortedv = []
        for b in list(self.get_all()):
            sortedv.append({"id": b.book_id, "days_rented": b.days_rented})
        sortedv = sorted(sortedv, key= \
            itemgetter("days_rented"), reverse=True)
        list_for_return = []
        for b in range(0, len(sortedv)):
            list_for_return.append(self.find_by_id(sortedv[b]["id"]))
        return list_for_return

    def sort_by_author(self):
        sortedv = []
        for b in list(self.get_all()):
            for i in sortedv:
                if len(sortedv) != 0 and i["author"] == b.author:
                    i["times_rented"] += b.times_rented
            else:
                sortedv.append({"author": b.author, "times_rented": b.times_rented})
        sortedv = sorted(sortedv, key= \
            itemgetter("times_rented"), reverse=True)
        list_for_return = []
        for b in range(0, len(sortedv)):
            list_for_return.append(
                "Author {0} with the books rented {1} times".format(sortedv[b]["author"], sortedv[b]["times_rented"]))
        return list_for_return

    def backup_op(self):
        self.__book_repository.backup_op()

    def undo_op(self):
        self.__book_repository.undo_op()

    def redo_op(self):
        self.__book_repository.redo_op()

    def exit_update_data(self):
        self.__book_repository.exit_update_data()

    def get_all(self):
        return self.__book_repository.get_all()

class ClientController(object):
    '''
    The bridge between the UI module and the Client Repository.
    '''
    def __init__(self, client_repository):
        self.__client_repository = client_repository  
    
    def find_by_id(self, client_id):
        return self.__client_repository[client_id]
    
    def find_client(self, client_field): #type: 2 - name
        list_for_print = []
        for c in list(self.get_all()):
            if client_field.replace(" ", "").lower() in c.name.replace(" ", "").lower():
                list_for_print.append(c)
        return list_for_print

    def add_client(self, client_id, name):
        if self.__client_repository[client_id] == None:
            self.backup_op()
            client = Client(client_id, name)
            self.__client_repository[client_id] = client
        else:
            raise DuplicateIdException("duplicate id {0}.".format(client_id))
    
    def delete_client(self, client_id):
        self.backup_op()
        del self[client_id]
        
    def update_client(self, client_id, name):
        client = Client(client_id, name)
        if self.__client_repository[client_id] is None:
            raise InexistentIdException("No client with id {0}.".format(client_id))
        if name != "":
            client.title = name
        self.backup_op()
        self.__client_repository[client_id] = client

    def sort_by_days(self):
        sortedv = []
        for c in list(self.get_all()):
            sortedv.append({"id": c.client_id, "days_rented": c.days_rented})
        sortedv = sorted(sortedv, key= \
            itemgetter("days_rented"), reverse=True)
        list_for_return = []
        for c in range(0, len(sortedv)):
            list_for_return.append(self.find_by_id(sortedv[c]["id"]))
        return list_for_return

    def backup_op(self):
        self.__client_repository.backup_op()

    def undo_op(self):
        self.__client_repository.undo_op()

    def redo_op(self):
        self.__client_repository.redo_op()

    def exit_update_data(self):
        self.__client_repository.exit_update_data()
        
    def get_all(self):
        return self.__client_repository.get_all()
    
class RentalController(object):
    '''
    The bridge between the UI module and the Rental Repository.
    '''
    def __init__(self, rental_repository, book_repository, client_repository):
        self.__rental_repository = rental_repository
        self.__book_repository = book_repository
        self.__client_repository = client_repository

    def date_to_class(self, string):
        string = string.split(".")
        day = int(string[0])
        month = int(string[1])
        year = int(string[2])
        final_date = date(year, month, day)
        return final_date

    def find_by_id(self, rental_id):
        return self.__rental_repository.find_by_id(rental_id)
    
    def add_rental(self, rental_id, book_id, client_id, rented, due):
        book = self.__book_repository.find_by_id(book_id)
        if book == None:
            book_id = -1
        if self.__client_repository.find_by_id(client_id) == None:
            client_id = -1
        rented = self.date_to_class(rented)
        due = self.date_to_class(due)
        returned = "Not returned"
        rental = Rental(rental_id, book_id, client_id, rented, due, returned)
        book.times_rented += 1
        self.__rental_repository.rent(rental)
    
    def return_rental(self, rental_id, returned):
        days_rented = 0
        returned = self.date_to_class(returned)
        rental = self.__rental_repository.find_by_id(rental_id)
        try:
            book_id = self.__book_repository.find_by_id(rental.book_id).book_id
            client_id = self.__client_repository.find_by_id(rental.client_id).client_id
        except AttributeError:
            print("Inexistent ID")
        if rental != None:
            days_rented += (date(returned.year, returned.month, returned.day) - \
                               date(rental.rented.year, rental.rented.month, rental.rented.day)).days
            self.__book_repository.find_by_id(book_id).days_rented += days_rented
            self.__client_repository.find_by_id(client_id).days_rented += days_rented
        self.__rental_repository.return_rental(rental_id, returned)

    def sort_overdue(self):
        sortedv = []
        for r in list(self.get_all()):
            if (date.today() > r.due and r.returned == "Not returned"):
                days_overdue = (date(date.today().year, date.today().month, date.today().day) - \
                                date(r.due.year, r.due.month, r.due.day)).days + r.overdue
                r.overdue = days_overdue
                sortedv.append({"id": r.rental_id, "days_overdue": days_overdue})
        sortedv = sorted(sortedv, key= \
            itemgetter("days_overdue"), reverse=True)
        list_for_return = []
        for r in range(0, len(sortedv)):
            #list_for_return.append(self.find_by_id(sortedv[r]["id"]))
            aux = str(self.__book_repository.find_by_id(self.find_by_id(sortedv[r]["id"]).book_id)) + " with overdue {0} days".\
                format(self.find_by_id(sortedv[r]["id"]).overdue)
            list_for_return.append(aux)
            #list_for_return.append(self.__book_repository.find_by_id(self.find_by_id(sortedv[r]["id"]).book_id))
        return list_for_return

    def backup_op(self):
        self.__rental_repository.backup_op()

    def undo_op(self):
        self.__client_repository.undo_op()

    def redo_op(self):
        self.__client_repository.redo_op()

    def exit_update_data(self):
        self.__rental_repository.exit_update_data()

    def get_all(self):
        return self.__rental_repository.get_all()