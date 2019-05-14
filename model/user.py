'''User model exist after authentication
it empty if not'''

import pymysql
from model import Database
from PyQt5.QtCore import QObject, pyqtSignal

class User(QObject):
    '''A user is connected to openfoodfacts_substitutes database'''

    status_connected = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
        self._connected = False

    def connect(self, username, password, family=None, nick=None):
        '''Connect User'''

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
            status = "{}\n{}".format(e.args[0], e.args[1])
            self.status_connected.emit(False, status)
        self._connected = True
        self.status_connected.emit(True, "Vous êtes connecté")

    @property
    def connected(self):
        '''Said if User is connected'''

        return self._connected

    @property
    def databse(self):
        '''Database property getter'''

        return self._database

