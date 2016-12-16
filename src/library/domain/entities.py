from datetime import date


class Book(object):
    '''
    Class of type book which holds an id, title, description and author.
    Getters and setters for all params.
    '''
    def __init__(self,book_id, title, description, author):
        self.__book_id = book_id
        self.__title = title
        self.__description = description
        self.__author = author
        self.__times_rented = 0
        self.__days_rented = 0
    
    ###ID
    @property
    def book_id(self):
        return self.__book_id

    ###TITLE
    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self,value):
        self.__title = value
        
     
    ###DESC   
    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, value):
        self.__description = value
        
    ###AUTH
    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, value):
        self.__author = value
    
    ###TIMES RENTED
    @property
    def times_rented(self):
        return self.__times_rented
    
    @times_rented.setter
    def times_rented(self, value):
        self.__times_rented = value
    
    ###DAYS RENTED
    @property
    def days_rented(self):
        return self.__days_rented
    
    @days_rented.setter
    def days_rented(self, value):
        self.__days_rented = value
    
    '''
    Function to overload print.
    '''
#     def __str__(self, *args, **kwargs):
#         return "(Book with id: {0}, title: {1}, description: {2}, author: {3})".format(self.book_id, self.title, self.description, self.author)
    def __str__(self, *args, **kwargs):
        return "Book with id: {0}, title: {1}, description: {2}, author: {3}, rented {4} times and {5} days"\
            .format(self.book_id, self.title, self.description, self.author, self.times_rented, self.days_rented)


class Client:
    '''
    Class of type client which holds an id, and name.
    Getters and setters for all params.
    '''
    def __init__(self,client_id, name):
        self.__client_id = client_id
        self.__name = name
        self.__days_rented = 0
    
    ###ID
    @property
    def client_id(self):
        return self.__client_id
    
    ###NAME
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def days_rented(self):
        return self.__days_rented

    @days_rented.setter
    def days_rented(self, value):
        self.__days_rented = value
    '''
    Function to overload print.
    '''
    def __str__(self, *args, **kwargs):
        return "Client with id: {0} and name: {1} with a total of {2} days rented.".format(self.client_id, self.name, self.days_rented)


class Rental:
    '''
    Class of type rental which holds an rental id, book id, client id, rented date, due date and returned state.
    Getters and setters for all params.
    '''
    def __init__(self, rental_id, book_id, client_id, rented, due, returned):
        self.__rental_id = rental_id
        self.__book_id = book_id
        self.__client_id = client_id
        self.__rented = rented
        self.__due = due
        self.__returned = returned
        self.__overdue = 0
        
    ###RENTALID
    @property
    def rental_id(self):
        return self.__rental_id
    
    ###BOOKID
    @property
    def book_id(self):
        return self.__book_id
    
    ###CLIENTID
    @property
    def client_id(self):
        return self.__client_id
    
    ###RENTED
    @property
    def rented(self):
        return self.__rented
    
    @rented.setter
    def rented(self, value):
        self.__rented = value
        
    ###DUE
    @property
    def due(self):
        return self.__due
    
    @due.setter
    def due(self, value):
        self.__due = value
    
    ###RETURNED
    @property
    def returned(self):
        return self.__returned
    
    @returned.setter
    def returned(self, value):
        self.__returned = value

    @property
    def overdue(self):
        return self.__overdue

    @overdue.setter
    def overdue(self, value):
        self.__overdue = value
    
    '''
    Function to overload print.
    '''
    def __str__(self, *args, **kwargs):
        if self.returned == "Not returned":
            return "Rental number {0}: Book with id {1}, rented to client with id {2} from date {3} to date {4} with overdue of: {5} days.".format(\
                self.rental_id, self.book_id, self.client_id, self.rented, self.due, (date.today() - date(self.__due.year, self.__due.month, self.__due.day)).days)
        else:
            return "Rental number {0}: Book with id {1}, was rented to client with id {2} from date {3} and returned on date {4}.".format(\
                self.rental_id, self.book_id, self.client_id, self.rented, self.returned)
#         if self.returned == 1:
#             return "(Rental number {0}: Book with id {1}, was rented to client with id {2} from date {3} and returned before date {4}.)".format(\
#                 self.rental_id, self.book_id, self.client_id, self.rented, self.due)
