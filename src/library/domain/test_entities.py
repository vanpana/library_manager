from unittest import TestCase

from library.domain.entities import Book, Client, Rental


class TestBook(TestCase):
    def setUp(self):
        super().setUp()
        self.__book = Book(1, "Title", "Description", "Author")

    def test_book_id(self):
        self.assertEqual(self.__book.book_id, 1, "Book ID should be 1!")

    def test_title(self):
        self.assertEqual(self.__book.title, "Title", "Book title should be Title!")
        self.__book.title = "Other title"
        self.assertEqual(self.__book.title, "Other title", "Book title should be Other title!")

    def test_description(self):
        self.assertEqual(self.__book.description, "Description", "Book title should be Description!")
        self.__book.description = "Other description"
        self.assertEqual(self.__book.description, "Other description", "Book title should be Other description!")

    def test_author(self):
        self.assertEqual(self.__book.author, "Author", "Book title should be Author!")
        self.__book.author = "Other author"
        self.assertEqual(self.__book.author, "Other author", "Book title should be Other author!")

    def test_times_rented(self):
        self.assertEqual(self.__book.times_rented, 0, "Times rented should be 0!")

    def test_days_rented(self):
        self.assertEqual(self.__book.days_rented, 0, "Days rented should be 0!")

class TestClient(TestCase):
    def setUp(self):
        super().setUp()
        self.__client = Client(1, "Name")

    def test_client_id(self):
        self.assertEqual(self.__client.client_id, 1, "The Client ID should be 1")

    def test_client_name(self):
        self.assertEqual(self.__client.name, "Name", "The client name should be Name")
        self.__client.name = "Other name"
        self.assertEqual(self.__client.name, "Other name", "The client name should be Other name")

class TestRental(TestCase):
    def setUp(self):
        super().setUp()
        self.__rental = Rental(1, 1, 1, "06.06.2016", "06.07.2016", 0)

    def test_rental_id(self):
        self.assertEqual(self.__rental.rental_id, 1, "The Rental ID should be 1")

    def test_book_id(self):
        self.assertEqual(self.__rental.book_id, 1, "Book ID should be 1!")

    def test_client_id(self):
        self.assertEqual(self.__rental.client_id, 1, "The Client ID should be 1")

    def test_rented_date(self):
        self.assertEqual(self.__rental.rented, "06.06.2016", "The rented date should be 06.06.2016")
        self.__rental.rented = "07.06.2016"
        self.assertEqual(self.__rental.rented, "07.06.2016", "The rented date should be 07.06.2016")

    def test_due_date(self):
        self.assertEqual(self.__rental.due, "06.07.2016", "The rented date should be 06.07.2016")
        self.__rental.due = "07.07.2016"
        self.assertEqual(self.__rental.due, "07.07.2016", "The rented date should be 07.07.2016")

    def test_returned(self):
        self.assertEqual(self.__rental.returned, 0, "The book should not be returned")
        self.__rental.returned = "07.07.2016"
        self.assertEqual(self.__rental.returned, "07.07.2016", "The book should be returned on 07.07.2016")