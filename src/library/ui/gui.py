from tkinter import *


class GUI(object):
    def __init__(self, book_controller, client_controller, rental_controller):
        self.__book_controller = book_controller
        self.__client_controller = client_controller
        self.__rental_controller = rental_controller

    def ui_loop(self):
        root = Tk()
        root.title("The library")

        last_op = []  # 1 - books, 2 - client, 3 - rental
        last_op_redo = []

        def book_mode():
            book_window = Toplevel()
            book_window.title("Book Entity")


            def add_options():
                add_window = Toplevel(book_window)
                add_window.title("Add new books")

                book_id_label = Label(add_window, text="Book ID")
                book_id = Entry(add_window)

                title_label = Label(add_window, text="Title")
                title = Entry(add_window)

                description_label = Label(add_window, text="Description")
                description = Entry(add_window)

                author_label = Label(add_window, text="Author")
                author = Entry(add_window)

                text = Label(add_window, text="Click to add your book")

                def submit_check():
                    text.config(
                        text="Book with id {0}, title {1}, description {2}, author {3} added!\n".format(book_id.get(),
                                                                                                        title.get(),
                                                                                                        description.get(),
                                                                                                        author.get()))
                    if book_id.get().strip(" ") != "" and title.get().strip(" ") != "" and description.get().strip(
                            " ") != "" and author.get().strip(" ") != "":
                        try:
                            self.__book_controller.add_book(int(book_id.get()), title.get(), description.get(),
                                                            author.get())
                            book_id.delete(0, END)
                            title.delete(0, END)
                            description.delete(0, END)
                            author.delete(0, END)
                            self.last_op += [1]
                        except ValueError:
                            text.config(text="ID must be an integer")
                        except Exception as ex:
                            text.config(text=ex)
                    else:
                        text.config(text="Fields can't be empty!")

                submit = Button(add_window, text="Add", command=submit_check)

                book_id_label.pack()
                book_id.pack()
                title_label.pack()
                title.pack()
                description_label.pack()
                description.pack()
                author_label.pack()
                author.pack()
                submit.pack()
                text.pack()

            def delete_book():
                delete_window = Toplevel(book_window)
                delete_window.title("Delete book by ID")

                book_id_label = Label(delete_window, text="Book ID")
                book_id = Entry(delete_window)

                text = Label(delete_window, text="Click to delete your book")

                def submit_check():
                    text.config(text="Book with id {0} deleted!\n".format(book_id.get()))
                    if book_id.get().strip(" ") != "":
                        try:
                            self.__book_controller.delete_book(int(book_id.get()))
                            book_id.delete(0, END)
                            self.last_op += [1]
                        except ValueError:
                            text.config(text="ID must be an integer")
                        except Exception as ex:
                            text.config(text=ex)

                submit = Button(delete_window, text="Delete", command=submit_check)
                submit.pack()
                text.pack()

                book_id_label.pack()
                book_id.pack()

            def update_book():
                update_window = Toplevel(book_window)
                update_window.title("Update existing books")

                book_id_label = Label(update_window, text="Book ID")
                book_id = Entry(update_window)

                title_label = Label(update_window, text="Title")
                title = Entry(update_window)
                description_label = Label(update_window, text="Description")
                description = Entry(update_window)

                author_label = Label(update_window, text="Author")
                author = Entry(update_window)

                text = Label(update_window, text="Click to update your book")

                def submit_check():
                    text.config(text="Book with id {0} updated!\n".format(book_id.get()))
                    if book_id.get().strip(" ") != "" and (title.get().strip(" ") != "" or description.get().strip(
                            " ") != "" or author.get().strip(" ") != ""):
                        try:
                            self.__book_controller.update_book(int(book_id.get()), title.get(), description.get(),
                                                               author.get())
                            book_id.delete(0, END)
                            title.delete(0, END)
                            description.delete(0, END)
                            author.delete(0, END)
                            self.last_op += [1]
                        except ValueError:
                            text.config(text="ID must be an integer")
                        except Exception as ex:
                            text.config(text=ex)
                    else:
                        text.config(text="Fields can't be empty!")

                submit = Button(update_window, text="Add", command=submit_check)

                book_id_label.pack()
                book_id.pack()
                title_label.pack()
                title.pack()
                description_label.pack()
                description.pack()
                author_label.pack()
                author.pack()
                submit.pack()
                text.pack()

            def search_book():
                search_window = Toplevel(book_window)
                search_window.title("Search a book")

                book_id_label = Label(search_window, text="Search by book ID")
                book_id = Entry(search_window)

                title_label = Label(search_window, text="Search by title")
                title = Entry(search_window)

                description_label = Label(search_window, text="Search by description")
                description = Entry(search_window)

                author_label = Label(search_window, text="Search by author")
                author = Entry(search_window)

                def submit_check():
                    if book_id.get() != "":
                        try:
                            book = self.__book_controller.find_by_id(int(book_id.get()))
                        except ValueError:
                            text.delete('1.0', END)
                            text.insert(END, "Input must be an integer!")

                        if book != None:
                            text.delete('1.0', END)
                            text.insert(END, book)
                        else:
                            text.delete('1.0', END)
                            text.insert(END, "Book with id {0} does not exist".format(book_id.get()))

                    elif title.get() != "":
                        text.delete('1.0', END)
                        for b in self.__book_controller.find_book(1,title.get()):
                            text.insert(END, b)
                            text.insert(END, "\n")

                    elif description.get() != "":
                        text.delete('1.0', END)
                        for b in self.__book_controller.find_book(2,description.get()):
                            text.insert(END, b)
                            text.insert(END, "\n")

                    elif author.get() != "":
                        text.delete('1.0', END)
                        for b in self.__book_controller.find_book(3,author.get()):
                            text.insert(END, b)
                            text.insert(END, "\n")


                submit = Button(search_window, text="Search", command=submit_check)

                text = Text(search_window)

                book_id_label.pack()
                book_id.pack()
                title_label.pack()
                title.pack()
                description_label.pack()
                description.pack()
                author_label.pack()
                author.pack()
                submit.pack()
                text.pack()

            def print_books():
                print_window = Toplevel(book_window)
                print_window.title("The list of the books")
                text = Text(print_window)
                text.pack()
                for b in self.__book_controller.get_all():
                    text.insert(END, b)
                    text.insert(END, "\n")

            def print_times_rented():
                print_window = Toplevel(book_window)
                print_window.title("List of the most rented")
                text = Text(print_window)
                text.pack()
                for b in self.__book_controller.sort_by_rents():
                    text.insert(END, b)
                    text.insert(END, "\n")

            def print_days_rented():
                print_window = Toplevel(book_window)
                print_window.title("List of the most rented")
                text = Text(print_window)
                text.pack()
                for b in self.__book_controller.sort_by_days():
                    text.insert(END, b)
                    text.insert(END, "\n")

            def print_days_author():
                print_window = Toplevel(book_window)
                print_window.title("List of the most rented author")
                text = Text(print_window)
                text.pack()
                for b in self.__book_controller.sort_by_author():
                    text.insert(END, b)
                    text.insert(END, "\n")


            add = Button(book_window, text="Add book", command=add_options)
            delete = Button(book_window, text="Delete book", command=delete_book)
            update = Button(book_window, text="Update book", command=update_book)
            search = Button(book_window, text="Seach book list", command=search_book)
            print = Button(book_window, text="Print book list", command=print_books)
            times_rented = Button(book_window, text="Print sorted list book by times rented", command=print_times_rented)
            days_rented = Button(book_window, text="Print sorted list book by days rented", command=print_days_rented)
            most_rented = Button(book_window, text="Print sorted list book by mosr rented authors", command=print_days_author)

            add.pack()
            delete.pack()
            update.pack()
            search.pack()
            print.pack()
            times_rented.pack()
            days_rented.pack()
            most_rented.pack()

        def client_mode():
            client_window = Toplevel()
            client_window.title("Client Entity")

            def add_client():
                add_window = Toplevel(client_window)
                add_window.title("Add new clients")

                client_id_label = Label(add_window, text="Client ID")
                client_id = Entry(add_window)

                name_label = Label(add_window, text="Name")
                name = Entry(add_window)

                text = Label(add_window, text="Click to add your client")

                def submit_check():
                    text.config(text="Client with id {0}, name {1} added!\n".format(client_id.get(), name.get()))
                    if client_id.get().strip(" ") != "" and name.get().strip(" "):
                        try:
                            self.__client_controller.add_client(int(client_id.get()), name.get())
                            client_id.delete(0, END)
                            name.delete(0, END)
                            self.last_op += [2]
                        except ValueError:
                            text.config(text="ID must be an integer")
                        except Exception as ex:
                            text.config(text=ex)
                    else:
                        text.config(text="Fields can't be empty!")

                submit = Button(add_window, text="Add", command=submit_check)

                client_id_label.pack()
                client_id.pack()
                name_label.pack()
                name.pack()
                submit.pack()
                text.pack()

            def delete_client():
                delete_window = Toplevel(client_window)
                delete_window.title("Delete client by ID")

                book_id_label = Label(delete_window, text="Client ID")
                book_id = Entry(delete_window)

                text = Label(delete_window, text="Click to delete your client")

                def submit_check():
                    text.config(text="Client with id {0} deleted!\n".format(book_id.get()))
                    if book_id.get().strip(" ") != "":
                        try:
                            self.__client_controller.delete_client(int(book_id.get()))
                            book_id.delete(0, END)
                            self.last_op += [2]
                        except ValueError:
                            text.config(text="ID must be an integer")
                        except Exception as ex:
                            text.config(text=ex)

                submit = Button(delete_window, text="Delete", command=submit_check)
                submit.pack()
                text.pack()

                book_id_label.pack()
                book_id.pack()

            def update_client():
                update_window = Toplevel(client_window)
                update_window.title("Update existing books")

                client_id_label = Label(update_window, text="Client ID")
                client_id = Entry(update_window)

                name_label = Label(update_window, text="Name")
                name = Entry(update_window)

                text = Label(update_window, text="Click to update your client")

                def submit_check():
                    text.config(text="Book with id {0} updated!\n".format(book_id.get()))
                    if client_id.get().strip(" ") != "" and (name.get().strip(" ") != ""):
                        try:
                            self.__book_controller.update_client(int(client_id.get()), name.get())
                            client_id.delete(0, END)
                            name.delete(0, END)
                            self.last_op += [2]
                        except ValueError:
                            text.config(text="ID must be an integer")
                        except Exception as ex:
                            text.config(text=ex)
                    else:
                        text.config(text="Fields can't be empty!")

                submit = Button(update_window, text="Add", command=submit_check)

                client_id_label.pack()
                client_id.pack()
                name_label.pack()
                name.pack()
                submit.pack()
                text.pack()

            def search_client():
                search_window = Toplevel(client_window)
                search_window.title("Search a client")

                book_id_label = Label(search_window, text="Search by client ID")
                book_id = Entry(search_window)

                title_label = Label(search_window, text="Search by name")
                title = Entry(search_window)

                def submit_check():
                    if book_id.get() != "":
                        try:
                            book = self.__client_controller.find_by_id(int(book_id.get()))
                        except ValueError:
                            text.delete('1.0', END)
                            text.insert(END, "Input must be an integer!")

                        if book != None:
                            text.delete('1.0', END)
                            text.insert(END, book)
                        else:
                            text.delete('1.0', END)
                            text.insert(END, "Client with id {0} does not exist".format(book_id.get()))

                    elif title.get() != "":
                        text.delete('1.0', END)
                        for b in self.__book_controller.find_book(1, title.get()):
                            text.insert(END, b)
                            text.insert(END, "\n")

                submit = Button(search_window, text="Search", command=submit_check)

                text = Text(search_window)

                book_id_label.pack()
                book_id.pack()
                title_label.pack()
                title.pack()
                submit.pack()
                text.pack()

            def print_clients():
                print_window = Toplevel(client_window)
                print_window.title("The list of the clients")
                text = Text(print_window)
                text.pack()
                for b in self.__client_controller.get_all():
                    text.insert(END, b)
                    text.insert(END, "\n")

            def print_days_rented():
                print_window = Toplevel(client_window)
                print_window.title("List of the most rented")
                text = Text(print_window)
                text.pack()
                for b in self.__client_controller.sort_by_days():
                    text.insert(END, b)
                    text.insert(END, "\n")

            add = Button(client_window, text="Add client", command=add_client)
            delete = Button(client_window, text="Delete client", command=delete_client)
            update = Button(client_window, text="Update client", command=update_client)
            search = Button(client_window, text="Seach client list", command=search_client)
            print = Button(client_window, text="Print client list", command=print_clients)
            days_rented = Button(client_window, text="Print sorted client list by days rented", command=print_days_rented)

            add.pack()
            delete.pack()
            update.pack()
            search.pack()
            print.pack()
            days_rented.pack()

        def rental_mode():
            rental_window = Toplevel()
            rental_window.title("Rentals")

            def add_rental():
                add_window = Toplevel(rental_window)
                add_window.title("Add new rentals")

                rental_id_label = Label(add_window, text="Rental ID")
                rental_id = Entry(add_window)

                book_id_label = Label(add_window, text="Client ID")
                book_id = Entry(add_window)

                client_id_label = Label(add_window, text="Client ID")
                client_id = Entry(add_window)

                rental_date_label = Label(add_window, text="Rental date (dd.mm.yyyy)")
                rental_date = Entry(add_window)

                due_date_label = Label(add_window, text="Due date (dd.mm.yyyy)")
                due_date = Entry(add_window)

                text = Label(add_window, text="Click to add your rental")

                def submit_check():
                    text.config(text="Rental with id {0}, book id {1}, client id {2} "
                                     "rented on {3} due {4} added!\n".format(rental_id.get(), book_id.get(), \
                                client_id.get(), rental_date.get(), due_date.get()))
                    if client_id.get().strip(" ") != "" and rental_id.get().strip(" "):
                        try:
                            self.__rental_controller.add_rental(int(rental_id.get()), int(book_id.get()),\
                                            int(client_id.get()), rental_date.get(), due_date.get())
                            rental_id.delete(0, END)
                            client_id.delete(0, END)
                            book_id.delete(0, END)
                            rental_date.delete(0, END)
                            due_date(0, END)
                            self.last_op += [3]
                        except ValueError:
                            text.config(text="ID must be an integer")
                        except Exception as ex:
                            text.config(text=ex)
                    else:
                        text.config(text="Fields can't be empty!")

                submit = Button(add_window, text="Add", command=submit_check)

                rental_id_label.pack()
                rental_id.pack()
                book_id_label.pack()
                book_id.pack()
                client_id_label.pack()
                client_id.pack()
                rental_date_label.pack()
                rental_date.pack()
                due_date_label.pack()
                due_date.pack()
                submit.pack()
                text.pack()

            def return_rental():
                return_window = Toplevel(rental_window)
                return_window.title("Add new rentals")

                rental_id_label = Label(return_window, text="Rental ID")
                rental_id = Entry(return_window)

                returned_label = Label(return_window, text="Returned date (dd.mm.yyyy)")
                returned = Entry(return_window)

                text = Label(return_window, text="Click to return rental")

                def submit_check():
                    text.config(text="Rental with id {0} returned!\n".format(rental_id.get()))
                    if rental_id.get().strip(" ") != "" and returned.get().strip(" "):
                        try:
                            self.__rental_controller.return_rental(int(rental_id.get()), returned.get())
                            rental_id.delete(0, END)
                            returned.delete(0, END)
                            self.last_op += [3]
                        except ValueError:
                            text.config(text="ID must be an integer")
                        except Exception as ex:
                            text.config(text=ex)
                    else:
                        text.config(text="Fields can't be empty!")

                submit = Button(return_window, text="Return", command=submit_check)

                rental_id_label.pack()
                rental_id.pack()
                returned_label.pack()
                returned.pack()
                submit.pack()

            def print_rentals():
                print_window = Toplevel(rental_window)
                print_window.title("The list of the rents")
                text = Text(print_window)
                text.pack()
                for b in self.__rental_controller.get_all():
                    text.insert(END, b)
                    text.insert(END, "\n")

            def print_overdues():
                print_window = Toplevel(rental_window)
                print_window.title("The list of the overdues")
                text = Text(print_window)
                text.pack()
                for b in self.__rental_controller.sort_overdue():
                    text.insert(END, b)
                    text.insert(END, "\n")

            add = Button(rental_window, text="Add rental", command=add_rental)
            delete = Button(rental_window, text="Return a book", command=return_rental)
            print = Button(rental_window, text="Print rental list", command=print_rentals)
            overdues = Button(rental_window, text="Print overdues",
                                 command=print_overdues)

            add.pack()
            delete.pack()
            print.pack()
            overdues.pack()

        def undo_op(last_op):
            if last_op == 1:
                self.__book_controller.undo_op()
            if last_op == 2:
                self.__client_controller.undo_op()
            if last_op == 3:
                self.__rental_controller.undo_op()

        def undo():
            if len(last_op) > 0:
                undo_op(last_op[len(last_op) - 1])
                self.last_op_redo += [last_op.pop()]

        def redo_op(last_op):
            if last_op == 1:
                self.__book_controller.redo_op()
            if last_op == 2:
                self.__client_controller.redo_op()
            if last_op == 3:
                self.__rental_controller.redo_op()

        def redo():
            if len(last_op_redo) > 0:
                redo_op(last_op_redo[len(last_op_redo) - 1])
                self.last_op += [last_op_redo.pop()]

        title = Label(text="Choose entity")
        book = Button(text="Book entity", command = book_mode)
        client = Button(text="Client entity", command = client_mode)
        rental = Button(text="Rental entity", command = rental_mode)
        undo = Button(text="Undo last operation", command = undo)
        redo = Button(text="Redo last operation", command = redo)

        title.pack()
        book.pack()
        client.pack()
        rental.pack()
        undo.pack()
        redo.pack()

        root.mainloop()

    def run_app(self):
        def test_data():
            '''
            Function that adds data before the start of the program
            '''
            ###BOOKS
            self.__book_controller.add_book(1, "First book", "The first one in the list", "A good author")
            self.__book_controller.add_book(2, "Second book", "The second in the list", "Another good author")
            self.__book_controller.add_book(5, "Third book with another ID", "Number five", "Another author")
            ###CLIENTS
            self.__client_controller.add_client(1, "Dorinel Panaite")
            self.__client_controller.add_client(2, "Client Test")
            ###RENTALS
            self.__rental_controller.add_rental(1, 1, 1, "05.6.2016", "07.8.2016")
            self.__rental_controller.add_rental(2, 2, 2, "05.6.2016", "07.8.2016")
            self.__rental_controller.return_rental(2, "07.8.2016")
            self.__rental_controller.return_rental(1, "03.8.2016")
            self.__rental_controller.add_rental(3, 2, 1, "09.8.2016", "10.8.2016")
            # self.__rental_controller.return_rental(3, 2, 1, "10.8.2016")
            # self.__rental_controller.add_rental(3, 2, 1, "08.12.2016", "09.12.2016")

        #test_data()
        self.ui_loop()
