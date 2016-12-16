import pickle
from datetime import date

from library.domain.entities import Book, Client, Rental
from library.repository.repo import BookRepository, ClientRepository, RentalRepository


class BookBinaryFileRepository(BookRepository):
    def __init__(self, validator_class, filename):
        super().__init__(validator_class)
        self.__filename = filename
        self.__load_data()
        super().backup_op()

    def __load_data(self):
        #TODO handle exceptions: no file, bad data
        with open(self.__filename, "rb") as f:
            try:
                books = pickle.load(f)
                for book in books:
                    super().save(book)
            except EOFError:
                return []

    def save(self, book):
        super().save(book)
        self.__save_to_file()

    def __save_to_file(self):
        with open(self.__filename, "wb") as f:
            pickle.dump(list(self.get_all()), f)

    def delete(self, book_id):
        super().delete(book_id)
        # self.__update_files()
        self.__save_to_file()

    def update(self, book_id, title, description, author):
        super().update(book_id, title, description, author)
        # self.__update_files()
        self.__save_to_file()

    def __update_files(self):
        with open(self.__filename, "w"):
            pass
        for b in super().get_all():
            self.__save_to_file(b)

    def exit_update_data(self):
        # self.__update_files()
        self.__save_to_file()

    def backup_op(self):
        super().backup_op()

    def undo(self):
        super().undo_op()
        # self.update_files()
        self.__save_to_file()

    def redo(self):
        super().redo_op()
        # self.update_files()
        self.__save_to_file()

class ClientBinaryFileRepository(ClientRepository):
    def __init__(self, validator_class, filename):
        super().__init__(validator_class)
        self.__filename = filename
        self.__load_data()
        super().backup_op()

    def __load_data(self):
        #TODO handle exceptions: no file, bad data
        with open(self.__filename, "rb") as f:
            try:
                clients = pickle.load(f)
                for client in clients:
                    super().save(client)
            except EOFError:
                return []

    def save(self, client):
        super().save(client)
        self.__save_to_file()

    def __save_to_file(self):
        with open(self.__filename, "wb") as f:
            pickle.dump(list(self.get_all()), f)

    def delete(self, client_id):
        super().delete(client_id)
        self.update_files()

    def update(self, client_id, name):
        super().update(client_id, name)
        # self.update_files()
        self.__save_to_file()

    def __update_files(self):
        with open(self.__filename, "w"):
            pass
        for c in super().get_all():
            self.__save_to_file(c)

    def exit_update_data(self):
        # self.__update_files()
        self.__save_to_file()

    def backup_op(self):
        super().backup_op()

    def undo(self):
        super().undo_op()
        # self.__update_files()
        self.__save_to_file()

    def redo(self):
        super().redo_op()
        # self.__update_files()
        self.__save_to_file()

class RentalBinaryFileRepository(RentalRepository):
    def __init__(self, validator_class, filename):
        super().__init__(validator_class)
        self.__filename = filename
        self.__load_data()
        super().backup_op()

    def __strtodate(self,a):
        return date(int(a.split("-")[0]), int(a.split("-")[1]), int(a.split("-")[2]))

    def __load_data(self):
        #TODO handle exceptions: no file, bad data
        with open(self.__filename, "rb") as f:
            try:
                rentals = pickle.load(f)
                for rental in rentals:
                    super().save(rental)
            except EOFError:
                return []

    def rent(self, rental):
        super().rent(rental)
        self.__save_to_file()

    def __save_to_file(self):
        with open(self.__filename, "wb") as f:
            pickle.dump(list(self.get_all()), f)

    def delete(self, rental_id):
        super().delete(rental_id)
        # self.__update_files()
        self.__save_to_file()

    def return_rental(self, rental_id, returned):
        super().return_rental(rental_id, returned)
        # self.__update_files()
        self.__save_to_file()

    def __update_files(self):
        with open(self.__filename, "w"):
            pass
        for c in super().get_all():
            self.__save_to_file(c)

    def exit_update_data(self):
        self.__update_files()

    def backup_op(self):
        super().backup_op()
        self.__save_to_file()
        #TODO Update if needed

    def undo(self):
        super().undo_op()
        self.__save_to_file()

    def redo(self):
        super().redo_op()
        self.__save_to_file()