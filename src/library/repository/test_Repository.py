from unittest import TestCase

from datetime import date

from library.controller.product_controller import BookController
from library.domain.entities import Book, Client, Rental
from library.domain.validators import LibraryValidator, LibraryException
from library.repository.repo import BookRepository, DuplicateIdException, InexistentIdException, ClientRepository, \
    RentalRepository

""" FOR CONTROLLER
    # def test_find(self):
    #     book = Book(1, "Title", "Description", "Author")
    #     self.__book_repository.save(book)
    #     self.assertEqual(self.__book_repository.find(1,"tl")[0].book_id, 1, "The result should be the book")
    #     self.assertEqual(self.__book_repository.find(2, "sc")[0].book_id, 1, "The result should be the book")
    #     self.assertEqual(self.__book_repository.find(3, "ut")[0].book_id, 1, "The result should be the book")

    # def test_sort_by_rents(self):
    #     book1 = Book(1, "Title", "Description", "Author")
    #     book2 = Book(2, "Title", "Description", "Author")
    #     self.__book_repository.save(book1)
    #     book1.times_rented = 5
    #     self.__book_repository.save(book2)
    #     self.assertEqual(self.__book_repository.sort_by_rents()[0].book_id, 1, "The result should be the book")


    # def test_sort_by_days(self):
    #     book1 = Book(1, "Title", "Description", "Author")
    #     book2 = Book(2, "Title", "Description", "Author")
    #     self.__book_repository.save(book1)
    #     book1.days_rented = 5
    #     self.__book_repository.save(book2)
    #     self.assertEqual(self.__book_repository.sort_by_days()[0].book_id, 1, "The result should be the book")
    #
    #
    # def test_sort_by_author(self):
    #     book1 = Book(1, "Title", "Description", "Author")
    #     book2 = Book(2, "Title", "Description", "Author")
    #     book3 = Book(3, "Title", "Description", "Auth")
    #     self.__book_repository.save(book1)
    #     self.__book_repository.save(book2)
    #     self.__book_repository.save(book3)
    #     book1.times_rented = 5
    #     book2.times_rented = 1
    #     book3.times_rented = 10
    #     self.assertEqual(self.__book_repository.sort_by_author()[0], "Author Auth with the books rended 10 times", "The result should be the book")
FOR CONTROLLER
"""

class TestBookRepository(TestCase):
    def setUp(self):
        super().setUp()
        self.__book_repository = BookRepository(LibraryValidator)

    def test_find_by_id(self):
        book = Book(1, "Title", "Description", "Author")
        self.__book_repository.save(book)
        self.assertEqual(self.__book_repository.find_by_id(1), book, "The book should exist")
        self.assertEqual(self.__book_repository.find_by_id(2), None, "The book should not exist")


    def test_save(self):
        book = Book(1, "Title", "Description", "Author")
        self.__book_repository.save(book)
        self.assertEqual(len(self.__book_repository.get_all()), 1, "There should be only 1 book")

        # check if duplicate id exception is raised
        book = Book(1, "Title", "Description", "Author")
        self.assertRaises(DuplicateIdException, self.__book_repository.save, book)

        # check if validator exception is raised
        book = Book("book", "Title", "Description", "Author")
        self.assertRaises(LibraryException, self.__book_repository.save, book)

    def test_delete(self):
        book = Book(1, "Title", "Description", "Author")
        self.__book_repository.save(book)
        self.__book_repository.delete(1)
        self.assertEqual(len(self.__book_repository.get_all()), 0, "There should be no books")

        # check if inexistent id exception is raised
        self.assertRaises(InexistentIdException, self.__book_repository.delete, 1)

    def test_update(self):
        book = Book(1, "Title", "Description", "Author")
        self.__book_repository.save(book)

        # tests if exception raised
        self.assertRaises(InexistentIdException, self.__book_repository.update, 5, "Title", "", "")

        self.__book_repository.update(1, "Other Title", "", "")
        self.assertEqual(book.title, "Other Title", "Title should have changed")

        self.__book_repository.update(1, "", "Other description", "")
        self.assertEqual(book.description, "Other description", "Description should have changed")

        self.__book_repository.update(1, "", "", "Other author")
        self.assertEqual(book.author, "Other author", "Author should have changed")

    def test_undo_op(self):
        book1 = Book(1, "Title", "Description", "Author")
        book2 = Book(2, "Title", "Description", "Author")
        book3 = Book(3, "Title", "Description", "Auth")
        self.__book_repository.backup_op()
        self.__book_repository.save(book1)
        self.__book_repository.backup_op()
        self.__book_repository.save(book2)
        self.__book_repository.backup_op()
        self.__book_repository.save(book3)
        self.__book_repository.undo_op()
        self.assertEqual(len(self.__book_repository.get_all()), 2, "Book 3 should have been deleted")

    def test_redo_op(self):
        book1 = Book(1, "Title", "Description", "Author")
        book2 = Book(2, "Title", "Description", "Author")
        book3 = Book(3, "Title", "Description", "Auth")
        self.__book_repository.backup_op()
        self.__book_repository.save(book1)
        self.__book_repository.backup_op()
        self.__book_repository.save(book2)
        self.__book_repository.backup_op()
        self.__book_repository.save(book3)
        self.__book_repository.undo_op()
        self.__book_repository.redo_op()
        self.assertEqual(len(self.__book_repository.get_all()), 3, "Book 3 should have been readded")

class TestClientRepository(TestCase):
    def setUp(self):
        super().setUp()
        self.__client_repository = ClientRepository(LibraryValidator)

    def test_find_by_id(self):
        client = Client(1, "Client")
        self.__client_repository.save(client)
        self.assertEqual(self.__client_repository.find_by_id(1), client, "The client should exist")
        self.assertEqual(self.__client_repository.find_by_id(2), None, "The client should not exist")

    def test_save(self):
        client = Client(1, "Client")
        self.__client_repository.save(client)
        self.assertEqual(len(self.__client_repository.get_all()), 1, "It should be only element")

        # check if exception is raised
        self.assertRaises(DuplicateIdException, self.__client_repository.save, client)

    def test_delete(self):
        client = Client(1, "Client")
        self.__client_repository.save(client)
        self.__client_repository.delete(1)
        self.assertEqual(len(self.__client_repository.get_all()), 0, "The element should have been deleted")

        # check if exception is raised
        self.assertRaises(InexistentIdException, self.__client_repository.delete, 1)

    def test_update(self):
        client = Client(1, "Client")
        self.__client_repository.save(client)
        self.__client_repository.update(1,"Other client")
        self.assertEqual(self.__client_repository.find_by_id(1).name, "Other client")

        # check if exception is raised
        self.assertRaises(InexistentIdException, self.__client_repository.update, 333, "")


    def test_undo_op(self):
        client = Client(1, "Client")
        self.__client_repository.backup_op()
        self.__client_repository.save(client)
        self.__client_repository.undo_op()
        self.assertEqual(len(self.__client_repository.get_all()), 0, "It should have undone")

    def test_redo_op(self):
        client = Client(1, "Client")
        self.__client_repository.backup_op()
        self.__client_repository.save(client)
        self.__client_repository.undo_op()
        #self.__client_repository.redo_op()
        # self.assertEqual(len(self.__client_repository.get_all()), 1, "It should have redone")

class TestRentalRepository(TestCase):
    def setUp(self):
        super().setUp()
        self.__rental_repository = RentalRepository(LibraryValidator)

    def test_find_by_id(self):
        rental = Rental(1, 1, 1, date(2016,6,16),date(2016,8,16), "Not returned")
        self.__rental_repository.rent(rental)
        self.assertEqual(self.__rental_repository.find_by_id(1).client_id, 1, "The client ID should be 1")

    def test_rent(self):
        rental = Rental(1,1,1,date(2016,6,16),date(2016,8,16),"Not returned")
        self.__rental_repository.rent(rental)
        self.assertEqual(len(self.__rental_repository.get_all()), 1, "A rental should already exist")

        # checks if inexistent book_id exception is raised
        self.assertRaises(InexistentIdException, self.__rental_repository.rent, Rental(1,-1,1,date(2016,6,16),date(2016,8,16),"Not returned"))

        # checks if book already rented exception
        self.assertRaises(DuplicateIdException, self.__rental_repository.rent,
                          Rental(1, 1, 1, date(2016,6,16),date(2016,8,16), "Not returned"))

        # check if client exists
        self.assertRaises(InexistentIdException, self.__rental_repository.rent,
                          Rental(2, 2, -1, date(2016,6,16),date(2016,8,16), "Not returned"))

        # check if duplicate rental
        self.assertRaises(DuplicateIdException, self.__rental_repository.rent, Rental(1,3,1,date(2016,6,16),date(2016,8,16),"Not returned"))

    def test_return_rental(self):
        rental = Rental(1, 1, 1, date(2016,6,16),date(2016,8,16), "Not returned")
        self.__rental_repository.rent(rental)
        self.__rental_repository.return_rental(1,date(2016,8,15))
        self.assertEqual(type(self.__rental_repository.find_by_id(1).returned), date, "Book should have been returned")

        # check if inexistent id exception
        self.assertRaises(InexistentIdException, self.__rental_repository.return_rental, 3, date(2016,8,16))

        # check if date after rental date
        self.assertRaises(DuplicateIdException, self.__rental_repository.return_rental, 1, date(2015,8,16))