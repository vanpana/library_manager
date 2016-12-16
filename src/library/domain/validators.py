class LibraryException(Exception):
    pass

class LibraryValidatorException(LibraryException):
    pass

class LibraryValidator(object):
    @staticmethod
    def validate_date(date):
        date.split(".")
        if len(date)!=3:
            raise LibraryValidatorException("Invalid date input!")
        try:
            date[0]=int(date[0])
            date[1]=int(date[1])
            date[2]=int(date[2])
        except Exception:
            raise LibraryValidatorException("Dates must be integers!")
        if date[0]<1 or date[0]>30:
            raise LibraryValidatorException("Invalid day input!")
        if date[1]<1 or date[1]>12:
            raise LibraryValidatorException("Invalid month input!")
                
    @staticmethod
    def validate_book(book):
        if not type(book.book_id) is int:
            raise LibraryValidatorException("ID must be an integer")
    
    @staticmethod
    def validate_client(client):
        if not type(client.client_id) is int:
            raise LibraryValidatorException("ID must be an integer")
    
    @staticmethod
    def validate_rental(rental):
        if not type(rental.rental_id) is int:
            raise LibraryValidatorException("Rental ID must be an integer")
        if not rental.rented < rental.due:
            raise LibraryValidatorException("Due day has to be greater than due day")