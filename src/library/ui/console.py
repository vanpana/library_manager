from time import sleep
import traceback

from library.domain.validators import LibraryException


class Console(object):
    '''
    Class that does the user input and output.
    '''
    def __init__(self, book_controller, client_controller, rental_controller):
        self.__book_controller = book_controller
        self.__client_controller = client_controller
        self.__rental_controller = rental_controller
    
    def print_entities(self):
        print("--------------------")
        print("Entities:")
        print("1: Book")
        print("2: Client")
        print("3: Rents")
        print("4: Undo last operation")
        print("5: Redo last operations")
        print("0: Exit")
    
    def print_options(self,mode):
        '''
        Function that returns the option for specific mode.
        '''
        options=0
        while True:
            if mode==0:
                return False
            if mode==1:
                print("1: Add a book")
                print("2: Delete a book by ID")
                print("3: Update book information by ID")
                print("4: Search book list")
                print("5: Print book list")
                print("6: Print sorted list book by times rented")
                print("7: Print sorted list book by days rented")
                print("8: Print sorted list book by mosr rented authors")
                while options not in [1,2,3,4,5,6,7,8]:
                    try:
                        options=int(input("Input command:"))
                    except Exception:
                        print("Command must be an integer")
                    if options not in [1,2,3,4,5,6,7,8]:
                        print("Command has to be 1, 2, 3, 4, 5, 6, 7 or 8!")
            elif mode==2:
                print("1: Add a client")
                print("2: Delete a client by ID")
                print("3: Update client information by ID")
                print("4: Search client list")
                print("5: Print client list")
                print("6: Print sorted list clients by days rented")
                while options not in [1,2,3,4,5,6]:
                    try:
                        options=int(input("Input command:"))
                    except Exception:
                        print("Command must be an integer")
                    if options not in [1,2,3,4,5,6]:
                        print("Command has to be 1, 2, 3, 4, 5 or 6!")

            elif mode==3:
                print("1: Rent a book")
                print("2: Return a book by rent ID")
                print("3: List all the rentals")
                print("4: List all the overdues")
                while options not in [1,2,3,4]:
                    try:
                        options=int(input("Input command:"))
                    except Exception:
                        print("Command must be an integer")
                    if options not in [1,2,3,4]:
                        print("Command has to be 1, 2, 3 or 4!")
            return options
    
    ###BOOKS###
    def ui_add_book(self):
        '''
        Function that gets the params from the user and executes the add function.
        '''
        while True:
            try:
                book_id = int(input("Input ID: "))
                break
            except ValueError:
                print("ID must be an integer!")
        while True:
            title = input("Input title: ")
            if title=="":
                print("Title can't be empty!")
            else:
                break
        while True:    
            description = input("Input description: ")
            if description=="":
                print("Description can't be empty!")
            else:
                break
        while True:
            author = input("Input author: ")
            if author=="":
                print("Author can't be empty!")
            else:
                break
        self.__book_controller.add_book(book_id, title, description, author)
    
    def ui_delete_book(self):
        '''
        Function that gets the params from the user and executes the delete function.
        '''
        while True:
            try:
                book_id = int(input("Input ID: "))
                break
            except ValueError:
                print("ID must be an integer!")
        self.__book_controller.delete_book(book_id)
        
    def ui_update_book(self):
        '''
        Function that gets the params from the user and executes the update function.
        '''
        while True:
            try:
                book_id = int(input("Input ID: "))
                break
            except ValueError:
                print("ID must be an integer!")
        title = input("Input title: ")
        description = input("Input description: ")
        author = input("Input author: ")
        self.__book_controller.update_book(book_id, title, description, author)
        
    def ui_find_book(self):
        options=0
        print("1: Find book by ID")
        print("2: Find book by title")
        print("3: Find book by description")
        print("4: Find book by author")
        while options not in [1,2,3,4]:
            try:
                options=int(input("Input command:"))
            except Exception:
                print("Command must be an integer")
            if options not in [1,2,3,4]:
                print("Command has to be 1, 2, 3 or 4!")
        if options == 1:
            while True:
                try:
                    find_id = int(input("Input ID: "))
                    break
                except ValueError:
                    print("Input must be an integer!")
            book = self.__book_controller.find_by_id(find_id)
            if book != None:
                print(book)
            else:
                print("Book with id {0} does not exist".format(find_id))
        else:
            options-=1
            search = input("Input search: ")
            while search == "":
                search = input("Search must not be empty! Input search: ")
            for p in self.__book_controller.find_book(options, search):
                print(p)
    
    def ui_list_book(self):
        '''
        Function that gets the params from the user and executes the listing function.
        '''
        for b in self.__book_controller.get_all():
            print(b)

    def ui_list_by_rented(self):
        for b in self.__book_controller.sort_by_rents():
             print(b)

    def ui_list_by_days(self):
        for b in self.__book_controller.sort_by_days():
            print(b)

    def ui_list_by_author(self):
        for b in self.__book_controller.sort_by_author():
            print(b)
    ###BOOKS###
    
    ###CLIENTS###
    def ui_add_client(self):
        '''
        Function that gets the params from the user and executes the add function.
        '''
        while True:
            try:
                client_id = int(input("Input ID: "))
                break
            except ValueError:
                print("ID must be an integer!")
        while True:
            name = input("Input name: ")
            if name=="":
                print("Title can't be empty!")
            else:
                break
        
        self.__client_controller.add_client(client_id, name)
        
    def ui_delete_client(self):
        '''
        Function that gets the params from the user and executes the delete function.
        '''
        while True:
            try:
                client_id = int(input("Input ID: "))
                break
            except ValueError:
                print("ID must be an integer!")
        self.__client_controller.delete_client(client_id)
    
    def ui_update_client(self):
        '''
        Function that gets the params from the user and executes the update function.
        '''
        while True:
            try:
                client_id = int(input("Input ID: "))
                break
            except ValueError:
                print("ID must be an integer!")
        name = input("Input name: ")
        self.__client_controller.update_client(client_id, name)
        
    def ui_find_client(self):
        options=0
        print("1: Find client by ID")
        print("2: Find client by name")
        while options not in [1,2]:
            try:
                options=int(input("Input command:"))
            except Exception:
                print("Command must be an integer")
            if options not in [1,2]:
                print("Command has to be 1 or 2!")
        if options == 1:
            while True:
                try:
                    find_id = int(input("Input ID: "))
                    break
                except ValueError:
                    print("Input must be an integer!")
            client = self.__client_controller.find_by_id(find_id)
            if client != None:
                print(client)
            else:
                print("Client with id {0} does not exist".format(find_id))
        else:
            search = input("Input search: ")
            while search == "":
                search = input("Search must not be empty! Input search: ")
            for c in self.__client_controller.find_client(search):
                print(c)
        
    def ui_list_client(self):
        '''
        Function that gets the params from the user and executes the listing function.
        '''
        for c in self.__client_controller.get_all():
            print(c)

    def ui_list_clients_by_days(self):
        for c in self.__client_controller.sort_by_days():
             print(c)
    ###CLIENTS###
    
    ###RENTS###
    def ui_rent_book(self):
        '''
        Function that gets the params from the user and executes the rent function.
        '''
        while True:
            try:
                rental_id = int(input("Input rental ID: "))
                break
            except ValueError:
                print("ID must be an integer!")
        
        while True:
            try:
                book_id = int(input("Input book ID: "))
                break
            except ValueError:
                print("ID must be an integer!")
                
        while True:
            try:
                client_id = int(input("Input client ID: "))
                break
            except ValueError:
                print("ID must be an integer!")
        
        while True: 
            rented = input("Input rental date (dd.mm.yyyy): ")
            if rented=="":
                print("Date can't be empty!")
            if "." not in rented or len(rented)!=10:
                print ("Invalid date input!")
            else:
                break
        
        while True: 
            due = input("Input due date (dd.mm.yyyy): ")
            if due=="":
                print("Date can't be empty!")
            if "." not in due or len(due)!=10:
                print ("Invalid date input!")
            else:
                break
        
        self.__rental_controller.add_rental(rental_id, book_id, client_id, rented, due)
    
    def ui_return_book(self):
        '''
        Function that gets the params from the user and executes the return function.
        '''
        while True:
            try:
                rental_id = int(input("Input rental ID: "))
                break
            except ValueError:
                print("ID must be an integer!")
        
        while True: 
            returned = input("Input returned date (dd.mm.yyyy): ")
            if returned=="":
                print("Date can't be empty!")
            if "." not in returned or len(returned)!=10:
                print ("Invalid date input!")
            else:
                break
        
        rental = self.__rental_controller.find_by_id(rental_id)
        self.__rental_controller.return_rental(rental_id, returned)
        
    def ui_list_rentals(self):
        '''
        Function that gets the params from the user and executes the listing function.
        '''
        for r in self.__rental_controller.get_all():
            print(r)

    def ui_print_overdues(self):
        for r in self.__rental_controller.sort_overdue():
            print(r)
    ###RENTS###

    def undo_op (self, last_op):
        if last_op == 1:
            self.__book_controller.undo_op()
        if last_op == 2:
            self.__client_controller.undo_op()
        if last_op == 3:
            self.__rental_controller.undo_op()

    def redo_op (self, last_op):
        if last_op == 1:
            self.__book_controller.redo_op()
        if last_op == 2:
            self.__client_controller.redo_op()
        if last_op == 3:
            self.__rental_controller.redo_op()
    
    def test_data(self):
        '''
        Function that adds data before the start of the program
        '''
        ###BOOKS
        self.__book_controller.add_book(1, "First book", "The first one in the list", "A good author")
        self.__book_controller.add_book(2, "Second book", "The second in the list", "Another good author")
        self.__book_controller.add_book(3, "Third book with another ID", "Number 3", "Another author")
        self.__book_controller.add_book(4, "Book 4", "Number 4", "Another author")
        self.__book_controller.add_book(5, "Book 5", "Number 5", "A good author")
        self.__book_controller.add_book(6, "Book 6", "Number 6", "A good author")
        self.__book_controller.add_book(7, "Book 7", "Number 7", "Another author")
        self.__book_controller.add_book(8, "Book 8", "Number 8", "A good author")
        self.__book_controller.add_book(9, "Book 9", "Number 9", "Another good author")
        self.__book_controller.add_book(10, "Book 10", "Number 10", "A good author")
        self.__book_controller.add_book(11, "Book 11", "Number 11", "Another good author")
        self.__book_controller.add_book(12, "Book 12", "Number 12", "Unknown author")
        self.__book_controller.add_book(13, "Book 13", "Number 13", "Unknown author")
        self.__book_controller.add_book(14, "Book 14", "Number 14", "Unknown author")
        self.__book_controller.add_book(15, "Book 15", "Number 15", "Another good author")
        ###CLIENTS
        self.__client_controller.add_client(1, "Dorinel Panaite")
        self.__client_controller.add_client(2, "Client Test")
        self.__client_controller.add_client(3, "Teodor Paius")
        self.__client_controller.add_client(4, "Another client")
        self.__client_controller.add_client(5, "Client fidel")
        self.__client_controller.add_client(6, "The best client")
        self.__client_controller.add_client(7, "The worst client")
        ###RENTALS
        self.__rental_controller.add_rental(1, 1, 1, "05.6.2016", "07.8.2016")
        self.__rental_controller.add_rental(2, 2, 2, "05.6.2016", "07.8.2016")
        self.__rental_controller.return_rental(2, "07.8.2016")
        self.__rental_controller.return_rental(1, "03.8.2016")
        self.__rental_controller.add_rental(3, 2, 1, "09.8.2016", "10.9.2016")
        self.__rental_controller.return_rental(3, "12.9.2016")
        self.__rental_controller.add_rental(4, 9, 5, "09.8.2016", "10.9.2016")
        self.__rental_controller.return_rental(4, "12.8.2016")
        self.__rental_controller.add_rental(5, 10, 5, "09.8.2016", "10.9.2016")
        self.__rental_controller.return_rental(5, "12.8.2016")
        self.__rental_controller.add_rental(6, 10, 5, "13.8.2016", "13.9.2016")


    def menuLoop(self):  
        '''
        Loop for printing the menu and inputting commands.
        '''
        options_books = {1: self.ui_add_book, 2: self.ui_delete_book, 3: self.ui_update_book, 4: self.ui_find_book,
                         5: self.ui_list_book, 6: self.ui_list_by_rented, 7: self.ui_list_by_days,
                         8: self.ui_list_by_author}
        options_client = {1: self.ui_add_client, 2: self.ui_delete_client, 3: self.ui_update_client,
                          4: self.ui_find_client, 5: self.ui_list_client, 6: self.ui_list_clients_by_days}
        options_rent = {1: self.ui_rent_book, 2: self.ui_return_book, 3: self.ui_list_rentals,
                        4: self.ui_print_overdues}
        last_op = []  # 1 - books, 2 - client, 3 - rental
        last_op_redo = []
        try:
            while True:       
                mode=-1
                self.print_entities()
                while mode not in [1,2,3,4,5,0]:
                    try:
                        mode=int(input("Choose entity:"))
                    except ValueError:
                        print("Input must be an integer")
                    if mode not in [1,2,3,4,5,0]:
                        raise LibraryException("Entity has to be 1, 2, 3, 4, 5 or 0!")

                if mode==4:
                    if len(last_op) > 0:
                        self.undo_op(last_op[len(last_op)-1])
                        last_op_redo += [last_op.pop()]

                elif mode==5:
                    if len(last_op_redo) > 0:
                        self.redo_op(last_op_redo[len(last_op_redo)-1])
                        last_op += [last_op_redo.pop()]

                else:
                    options=self.print_options(mode)

                    if options==0:
                        self.__book_controller.exit_update_data()
                        self.__client_controller.exit_update_data()
                        self.__rental_controller.exit_update_data()
                        print("\nApplication ended")
                        return False

                    if mode==1:
                        if options in [1,2,3]:
                            last_op += [1]
                        options_books[options]()

                    elif mode==2:
                        if options in [1,2,3]:
                            last_op += [2]
                        options_client[options]()

                    elif mode==3:
                        if options in [1,2]:
                            last_op += [3]
                        options_rent[options]()

                sleep(0.7)
                    
        except LibraryException as se:
            print("exception when executing command: ", se)
            traceback.print_exc()

        except KeyboardInterrupt:
            self.__book_controller.exit_update_data()
            self.__client_controller.exit_update_data()
            self.__rental_controller.exit_update_data()
            print("\nApplication ended")
            return False


              
    def run_console(self):    
        '''
        Function for looping the program till exit command
        '''
        self.test_data()
        while True:
            if self.menuLoop() == False:
                break
        