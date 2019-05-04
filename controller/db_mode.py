'''Controller for Daytabase mode'''

from model import Database
from view import MainWindow

class DatabaseMode():
    ''' Print/record data inside local database'''

    def __init__(self, window, database):
        self.window = window
        self.database = database

