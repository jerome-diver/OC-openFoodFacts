'''User model exist after authentication
it empty if not'''

import pymysql
from PyQt5.QtCore import QObject, pyqtSignal

from settings import DEBUG_MODE
from model import Database

class User(QObject):
    '''A user is connected to openfoodfacts_substitutes database'''

    status_connected = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
        self._connected = False
        self._family = ""
        self._nick = ""
        self._username = ""
        self._id = ""
        self._database = None

    def connect(self, username, password, family=None, nick=None):
        '''Connect User'''

        self._family = family
        self._nick = nick
        self._username = username
        self._database = None
        try:
            self._database = Database(username,
                                      password,
                                      'openfoodfacts_substitutes')
        except pymysql.err.OperationalError as error:
            status = "{}\n{}".format(error.args[0], error.args[1])
            self.status_connected.emit(False, status)
        self._connected = True
        self.status_connected.emit(True, "Vous êtes connecté")
        request = "SELECT id, nick_name, family_name FROM users " \
                  "WHERE username = %s;"
        for row in self._database.ask_request(request, self._username):
            self._id = row["id"]
            self._family = row["family_name"]
            self._nick = row["nick_name"]
        if DEBUG_MODE:
            print(self._nick, self._family)

    def disconnect(self):
        '''disconnectuser to local database'''

        self._database.disconnect_database()

    @property
    def connected(self):
        '''Said if User is connected'''

        return self._connected

    @property
    def database(self):
        '''Database property getter'''

        return self._database

    @property
    def id(self):
        '''Return id of user'''

        return self._id

    @property
    def family(self):
        '''Return self._family'''

        return self._family

    @property
    def nick(self):
        '''Return self._nick'''

        return self._nick

    @property
    def username(self):
        '''Return self._username'''

        return self._username
