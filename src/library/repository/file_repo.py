from datetime import date

from library.domain.entities import Book, Client, Rental
from library.repository.repo import BookRepository, ClientRepository, RentalRepository


class BookFileRepository(BookRepository):
    def __init__(self, validator_class, filename):
        super().__init__(validator_class)
        self.__filename = filename
        self.__load_data()
        super().backup_op()

    def __load_data(self):
        #TODO handle exceptions: no file, bad data
        with open(self.__filename) as f:
            for line in f:
                book = line.split(",")
                if book != None:
                    times_rented = int(book[4])
                    days_rented = int(book[5])
                    book = Book(int(book[0]), book[1], book[2], book[3])
                    book.times_rented = times_rented
                    book.days_rented = days_rented
                    super().save(book)

    def save(self, book):
        super().save(book)
        self.__save_to_file(book)

    def __save_to_file(self, book):
        with open(self.__filename, "a") as f:
            f.write("{0},{1},{2},{3},{4},{5},\n".format(book.book_id, book.title, book.description, book.author,\
                                                        book.times_rented, book.days_rented))

    def delete(self, book_id):
        super().delete(book_id)
        self.__update_files()

    def update(self, book_id, title, description, author):
        super().update(book_id, title, description, author)
        self.__update_files()

    def __update_files(self):
        with open(self.__filename, "w"):
            pass
        for b in super().get_all():
            self.__save_to_file(b)

    def exit_update_data(self):
        self.__update_files()

    def backup_op(self):
        super().backup_op()

    def undo(self):
        super().undo_op()
        self.__update_files()

    def redo(self):
        super().redo_op()
        self.__update_files()

class ClientFileRepository(ClientRepository):
    def __init__(self, validator_class, filename):
        super().__init__(validator_class)
        self.__filename = filename
        self.__load_data()
        super().backup_op()

    def __load_data(self):
        #TODO handle exceptions: no file, bad data
        with open(self.__filename) as f:
            for line in f:
                client = line.split(",")
                if client != None:
                    client = Client(int(client[0]), client[1])
                    super().save(client)

    def save(self, client):
        super().save(client)
        self.__save_to_file(client)

    def __save_to_file(self, client):
        with open(self.__filename, "a") as f:
            f.write("{0},{1},{2},\n".format(client.client_id, client.name, client.days_rented))

    def delete(self, client_id):
        super().delete(client_id)
        self.update_files()

    def update(self, client_id, name):
        super().update(client_id, name)
        self.update_files()

    def __update_files(self):
        with open(self.__filename, "w"):
            pass
        for c in super().get_all():
            self.__save_to_file(c)

    def exit_update_data(self):
        self.__update_files()

    def backup_op(self):
        super().backup_op()

    def undo(self):
        super().undo_op()
        self.__update_files()

    def redo(self):
        super().redo_op()
        self.__update_files()

class RentalFileRepository(RentalRepository):
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
                rental = line.split(",")
                if rental != None:
                    if rental[5] != "Not returned":
                        rental = Rental(int(rental[0]), int(rental[1]), int(rental[2]),  self.__strtodate(rental[3]), \
                            self.__strtodate(rental[4]), self.__strtodate(rental[5]))
                        super().rent(rental)
                        super().return_rental(rental.rental_id,rental.returned)
                    else:
                        rental = Rental(int(rental[0]), int(rental[1]), int(rental[2]), self.__strtodate(rental[3]),\
                                        self.__strtodate(rental[4]), "Not returned")
                        super().rent(rental)

    def rent(self, rental):
        super().rent(rental)
        self.__save_to_file(rental)

    def __save_to_file(self, rental):
        with open(self.__filename, "a") as f:
            f.write("{0},{1},{2},{3},{4},{5},\n".format(rental.rental_id, rental.book_id, rental.client_id, rental.rented,\
                                                        rental.due, rental.returned))

    def delete(self, rental_id):
        super().delete(rental_id)
        self.__update_files()

    def return_rental(self, rental_id, returned):
        super().return_rental(rental_id, returned)
        self.__update_files()


    def __update_files(self):
        with open(self.__filename, "w"):
            pass
        for c in super().get_all():
            self.__save_to_file(c)

    def exit_update_data(self):
        self.__update_files()

    def backup_op(self):
        super().backup_op()

    def undo(self):
        super().undo_op()
        self.__update_files()

    def redo(self):
        super().redo_op()
        self.__update_files()