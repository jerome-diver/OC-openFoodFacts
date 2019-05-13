'''User model exist after authentication
it empty if not'''

import pymysql
from model import Database
from PyQt5.QtCore import QObject, pyqtSignal

class User(QObject):
    '''A user is connected to openfoodfacts_substitutes database'''

    status_connected = pyqtSignal(bool)

    def __init__(self, username, password, family=None, nick=None):
        self._family = family
        self._nick = nick
        self._username = username
        self.substitutes_selections = []
        self._database = None
        try:
            self._database = Database(username,
                                password,
                                'openfoodfacts_substitutes')
        except pymysql.err.OperationalError as e:
            self.status_connected.emit(False)
        self.status_connected.emit(True)

    @property
    def databse(self):
        '''Database property getter'''

        return self._database

