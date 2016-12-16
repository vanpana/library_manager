from datetime import date

from library.domain.entities import Book, Client, Rental
from library.repository.repo import BookRepository, ClientRepository, RentalRepository

import json

class BookJsonFileRepository(BookRepository):
    def __init__(self, validator_class, filename):
        super().__init__(validator_class)
        self.__filename = filename
        self.__load_data()
        super().backup_op()

    def __load_data(self):
        #TODO handle exceptions: no file, bad data
        with open(self.__filename) as f:
            for line in f:
                line = json.loads(line.strip("'"))
                for book in line:
                    times_rented = int(book["times_rented"])
                    days_rented = int(book["days_rented"])
                    book = Book(int(book["book_id"]), book["title"], book["description"], book["author"])
                    book.times_rented = times_rented
                    book.days_rented = days_rented
                    super().save(book)

    def save(self, book):
        super().save(book)
        self.__save_to_file()

    def __save_to_file(self):
        all = []
        for book in super().get_all():
            all.append({"book_id": book.book_id, "title": book.title, "description": book.description, "author": book.author, \
                        "times_rented": book.times_rented, "days_rented": book.days_rented})
        dump = json.dumps(all)
        with open(self.__filename, "w") as f:
            f.write(dump)

    def delete(self, book_id):
        super().delete(book_id)
        self.__save_to_file()

    def update(self, book_id, title, description, author):
        super().update(book_id, title, description, author)
        self.__save_to_file()

    def exit_update_data(self):
        self.__save_to_file()

    def backup_op(self):
        super().backup_op()

    def undo(self):
        super().undo_op()
        self.update_files()

    def redo(self):
        super().redo_op()
        self.update_files()

class ClientJsonFileRepository(ClientRepository):
    def __init__(self, validator_class, filename):
        super().__init__(validator_class)
        self.__filename = filename
        self.__load_data()
        super().backup_op()

    def __load_data(self):
        #TODO handle exceptions: no file, bad data
        with open(self.__filename) as f:
            for line in f:
                line = json.loads(line.strip("'"))
                for client in line:
                    client = Client(int(client["client_id"]), client["name"])
                    super().save(client)

    def save(self, client):
        super().save(client)
        self.__save_to_file(client)

    def __save_to_file(self):
        all = []
        for client in super().get_all():
            all.append({"client_id": client.client_id, "name": client.name, "days_rented": client.days_rented})
        dump = json.dumps(all)
        with open(self.__filename, "w") as f:
            f.write(dump)

    def delete(self, client_id):
        super().delete(client_id)
        self.__save_to_file()

    def update(self, client_id, name):
        super().update(client_id, name)
        self.__save_to_file()

    def exit_update_data(self):
        self.__save_to_file()

    def backup_op(self):
        super().backup_op()

    def undo(self):
        super().undo_op()
        self.__save_to_file()

    def redo(self):
        super().redo_op()
        self.__save_to_file()

class RentalJsonFileRepository(RentalRepository):
    def __init__(self, validator_class, filename):
        super().__init__(validator_class)
        self.__filename = filename
        self.__load_data()
        super().backup_op()

    def __strtodate(self,a):
        return date(int(a.split("-")[0]), int(a.split("-")[1]), int(a.split("-")[2]))

    def __load_data(self):
        #TODO handle exceptions: no file, bad data
        with open(self.__filename) as f:
            for line in f:
                line = json.loads(line.strip("'"))
                for rental in line:
                    if rental["returned"] != "Not returned":
                        rental = Rental(int(rental["rental_id"]), int(rental["book_id"]), int(rental["client_id"]),\
                                        self.__strtodate(rental["rented"]), \
                            self.__strtodate(rental["due"]), self.__strtodate(rental["returned"]))
                        super().rent(rental)
                        super().return_rental(rental.rental_id,rental.returned)
                    else:
                        rental = Rental(int(rental["rental_id"]), int(rental["book_id"]), int(rental["client_id"]),\
                                        self.__strtodate(rental["rented"]),\
                                        self.__strtodate(rental["due"]), "Not returned")
                        super().rent(rental)

    def rent(self, rental):
        super().rent(rental)
        self.__save_to_file(rental)

    def __save_to_file(self):
        all = []
        for rental in super().get_all():
            all.append({"rental_id": rental.rental_id, "book_id": rental.book_id, "client_id": rental.client_id,\
                        "author": rental.rented, "times_rented": rental.due, "days_rented": rental.returned})
        dump = json.dumps(all)
        with open(self.__filename, "w") as f:
            f.write(dump)

    def delete(self, rental_id):
        super().delete(rental_id)
        self.__save_to_file()

    def return_rental(self, rental_id, returned):
        super().return_rental(rental_id, returned)
        self.__save_to_file()

    def exit_update_data(self):
        self.__save_to_file()

    def backup_op(self):
        super().backup_op()

    def undo(self):
        super().undo_op()
        self.__save_to_file()

    def redo(self):
        super().redo_op()
        self.__save_to_file()