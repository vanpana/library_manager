'''
Created on Nov 3, 2016

@author: vanpana
'''
import os
import pickle
from tkinter import *


import traceback

from library.controller.product_controller import BookController,\
    ClientController, RentalController
from library.domain.validators import LibraryValidator
from library.repository.binary_repo import BookBinaryFileRepository, ClientBinaryFileRepository, \
    RentalBinaryFileRepository
from library.repository.file_repo import BookFileRepository, RentalFileRepository, ClientFileRepository
from library.repository.json_repo import BookJsonFileRepository, ClientJsonFileRepository, RentalJsonFileRepository
from library.repository.repo import BookRepository, ClientRepository,\
    RentalRepository
from library.repository.sql_repo import BookSqlFileRepository, ClientSqlFileRepository
from library.ui.console import Console
from library.ui.gui import GUI

class Settings(object):
    def __init__(self, filename):
        self.__filename = filename
        self.__repository = None
        self.__books = None
        self.__clients = None
        self.__rentals = None
        self.__ui = None
        self.__load_data()

    def __load_data(self):
        with open(self.__filename) as f:
            for line in f:
                line = line.strip("\n")
                line = line.split(" ")
                if line[0] == "repository":
                    self.__repository = line[2]
                elif line[0] == "books":
                    self.__books = line[2][1:-1]
                elif line[0] == "clients":
                    self.__clients = line[2][1:-1]
                elif line[0] == "rentals":
                    self.__rentals = line[2][1:-1]
                elif line[0] == "ui":
                    self.__ui = line[2]
    @property
    def repository(self):
        return self.__repository

    @property
    def books(self):
        return self.__books

    @property
    def clients(self):
        return self.__clients

    @property
    def rentals(self):
        return self.__rentals

    @property
    def ui(self):
        return self.__ui

if __name__ == '__main__':

    try:

        '''
        Main function where all the initialisations are done and app loop starts
        '''
        book_controller, client_controller, rental_controller = None, None, None

        settings = Settings("./settings.properties")
        settings = [settings.repository, settings.books, settings.clients, settings.rentals, settings.ui]

        if (settings[0] == 'textfiles' or settings[0] == 'binaryfiles') and (settings[1] == None or \
                                                                             settings[2] == None or \
                                                                             settings[3] == None):
            print("Settings file not configured properly!")
        else:
            if settings[0] == 'inmemory':
                book_repository = BookRepository(LibraryValidator)
                client_repository = ClientRepository(LibraryValidator)
                rental_repository = RentalRepository(LibraryValidator)

            elif settings[0] == 'textfiles':
                book_repository = BookFileRepository(LibraryValidator, settings[1])
                client_repository = ClientFileRepository(LibraryValidator, settings[2])
                rental_repository = RentalFileRepository(LibraryValidator, settings[3])

            elif settings[0] == 'binaryfiles':
                book_repository = BookBinaryFileRepository(LibraryValidator, settings[1])
                client_repository = ClientBinaryFileRepository(LibraryValidator, settings[2])
                rental_repository = RentalBinaryFileRepository(LibraryValidator, settings[3])

            elif settings[0] == 'jsonfiles':
                book_repository = BookJsonFileRepository(LibraryValidator, settings[1])
                client_repository = ClientJsonFileRepository(LibraryValidator, settings[2])
                rental_repository = RentalJsonFileRepository(LibraryValidator, settings[3])

            elif settings[0] == 'sqlfiles':
                book_repository = BookSqlFileRepository(LibraryValidator, settings[1])
                client_repository = ClientSqlFileRepository(LibraryValidator, settings[2])
                rental_repository = RentalJsonFileRepository(LibraryValidator, settings[3])

            book_controller = BookController(book_repository)
            client_controller = ClientController(client_repository)
            rental_controller = RentalController(rental_repository,  book_repository, client_repository)

            if settings[4] == None or settings[4] == 'console':
                console = Console(book_controller, client_controller, rental_controller)
                console.run_console()

            elif settings[4] == 'gui':
                gui = GUI(book_controller, client_controller, rental_controller)
                gui.run_app()

    except Exception as ex:
        print("exception: ", ex)
        traceback.print_exc()