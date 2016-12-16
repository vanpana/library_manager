from library.domain.entities import Book, Client, Rental
from library.repository.repo import BookRepository, ClientRepository
import sqlite3

class BookSqlFileRepository(BookRepository):
    def __init__(self, validator_class, filename):
        super().__init__(validator_class)
        self.__filename = filename
        self.__load_data()
        super().backup_op()

    def __load_data(self):
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        c.execute('''CREATE TABLE if not EXISTS books
                     (book_id int, title varchar(255), description varchar(255), author varchar(255), \
                     times_rented int, days_rented int, PRIMARY KEY(book_id))''')

        c.execute("SELECT * FROM books")

        book = c.fetchone()
        while book != None:
            times_rented = int(book[4])
            days_rented = int(book[5])
            book = Book(int(book[0]), book[1], book[2], book[3])
            book.times_rented = times_rented
            book.days_rented = days_rented
            super().save(book)
            book = c.fetchone()

        conn.commit()
        conn.close()

    def save(self, book):
        super().save(book)
        self.__save_to_file(book)

    def __save_to_file(self, book):
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        c.execute("INSERT INTO books VALUES (?,?,?,?,?,?)", [book.book_id, book.title, book.description, book.author,\
                  book.times_rented, book.days_rented])

        conn.commit()
        conn.close()

    def update(self, book_id, title, description, author):
        super().update(book_id, title, description, author)
        self.__update_files()

    def __update_files(self):
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        for book in super().get_all():
            c.execute("UPDATE books set title = (?), description = (?), author = (?), times_rented = (?), \
                      days_rented = (?) where book_id=(?)",[book.title, book.description, book.author,\
                  book.times_rented, book.days_rented, book.book_id])

        conn.commit()
        conn.close()

    def delete(self, book_id):
        super().delete(book_id)
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        c.execute("DELETE FROM books where book_id=(?)", [book_id])

        conn.commit()
        conn.close()

    def exit_update_data(self):
        self.__update_files()

    def __delete_and_create(self):
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        c.execute("DELETE FROM books where book_id != 'abc'")
        for book in super().get_all():
            self.__save_to_file(book)

        conn.commit()
        conn.close()

    def backup_op(self):
        super().backup_op()

    def undo(self):
        super().undo_op()
        self.__delete_and_create()

    def redo(self):
        super().redo_op()
        self.__delete_and_create()


class ClientSqlFileRepository(ClientRepository):
    def __init__(self, validator_class, filename):
        super().__init__(validator_class)
        self.__filename = filename
        self.__load_data()
        super().backup_op()

    def __load_data(self):
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        c.execute('''CREATE TABLE if not EXISTS clients
                     (client_id int, name varchar(255), days_rented int, PRIMARY KEY(client_id))''')

        c.execute("SELECT * FROM clients")

        client = c.fetchone()
        while client != None:
            days_rented = int(client[2])
            client = Client(int(client[0]), client[1])
            client.days_rented = days_rented
            super().save(client)
            client = c.fetchone()

        conn.commit()
        conn.close()

    def save(self, client):
        super().save(client)
        self.__save_to_file(client)

    def __save_to_file(self, client):
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        c.execute("INSERT INTO clients VALUES (?,?,?)", [client.client_id, client.name, client.days_rented])

        conn.commit()
        conn.close()

    def update(self, client_id, name):
        super().update(client_id, name)
        self.__update_files()

    def __update_files(self):
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        for client in super().get_all():
            c.execute("UPDATE clients set name = (?), days_rented = (?) where book_id=(?)",\
                      [client.name, client.days_rented, client.client_id])

        conn.commit()
        conn.close()

    def delete(self, client_id):
        super().delete(client_id)
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        c.execute("DELETE FROM clients where client_id=(?)", [client_id])

        conn.commit()
        conn.close()

    def __delete_and_create(self):
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        c.execute("DELETE FROM clients where client_id != 'abc'")
        for book in super().get_all():
            self.__save_to_file(book)

        conn.commit()
        conn.close()

    def exit_update_data(self):
        self.__update_files()

    def backup_op(self):
        super().backup_op()

    def undo(self):
        super().undo_op()
        self.__delete_and_create()

    def redo(self):
        super().redo_op()
        self.__delete_and_create()

class RentalSqlFileRepository(ClientRepository):
    def __init__(self, validator_class, filename):
        super().__init__(validator_class)
        self.__filename = filename
        self.__load_data()
        super().backup_op()

    def __load_data(self):
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        c.execute('''CREATE TABLE if not EXISTS rentals
                     (rental_id int, book_id int, client_id int, rented varchar(255), due varchar(255), \
                     returned varchar(255), PRIMARY KEY(rental_id))''')

        c.execute("SELECT * FROM rentals")

        rental = c.fetchone()
        while rental != None:
            if rental[5] != "Not returned":
                rental = Rental(int(rental[0]), int(rental[1]), int(rental[2]), self.__strtodate(rental[3]), \
                                self.__strtodate(rental[4]), self.__strtodate(rental[5]))
                super().rent(rental)
                super().return_rental(rental.rental_id, rental.returned)
            else:
                rental = Rental(int(rental[0]), int(rental[1]), int(rental[2]), self.__strtodate(rental[3]), \
                                self.__strtodate(rental[4]), "Not returned")
                super().rent(rental)
            super().save(rental)
            rental = c.fetchone()

        conn.commit()
        conn.close()

    def save(self, rental):
        super().save(rental)
        self.__save_to_file(rental)

    def __save_to_file(self, rental):
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        c.execute("INSERT INTO rentals VALUES (?,?,?,?,?,?)", [rental.rental_id, rental.book_id, rental.client_id, \
                                                               rental.rented, rental.due, rental.returned])

        conn.commit()
        conn.close()

    def update(self, client_id, name):
        super().update(client_id, name)
        self.__update_files()

    def __update_files(self):
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        for client in super().get_all():
            c.execute("UPDATE clients set name = (?), days_rented = (?) where book_id=(?)",\
                      [client.name, client.days_rented, client.client_id])

        conn.commit()
        conn.close()

    def delete(self, client_id):
        super().delete(client_id)
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        c.execute("DELETE FROM clients where client_id=(?)", [client_id])

        conn.commit()
        conn.close()

    def __delete_and_create(self):
        conn = sqlite3.connect(self.__filename)
        c = conn.cursor()

        c.execute("DELETE FROM clients where client_id != 'abc'")
        for book in super().get_all():
            self.__save_to_file(book)

        conn.commit()
        conn.close()

    def exit_update_data(self):
        self.__update_files()

    def backup_op(self):
        super().backup_op()

    def undo(self):
        super().undo_op()
        self.__delete_and_create()

    def redo(self):
        super().redo_op()
        self.__delete_and_create()