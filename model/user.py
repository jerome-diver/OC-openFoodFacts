"""User model exist after authentication
it empty if not"""

import pymysql
from PyQt5.QtCore import QObject, pyqtSignal

from model import AdminConnection
from settings import DEBUG_MODE


class User(QObject):
    """A user is connected to openfoodfacts_substitutes database"""

    status_connection = pyqtSignal(bool, str)

    def __init__(self, connection):
        super().__init__()
        self._connection = connection
        if DEBUG_MODE:
            nature = "Admin" if self.is_admin() else "normal"
            print("=====  U S E R  ( new", nature, ") =====")
        self._family = ""
        self._nick = ""
        self._username = ""
        self._id = ""

    def connect(self, username, password, family=None, nick=None):
        """Connect User"""

        if not self.is_admin() and not self.is_connected():
            try:
                self._connection.connect(
                    username,
                    password,
                    'openfoodfacts_substitutes')
            except pymysql.err.OperationalError as error:
                status = "{}\n{}".format(error.args[0], error.args[1])
                self.status_connection.emit(False, status)
            else:
                self._family = family
                self._nick = nick
                self._username = username
                try:
                    request = "SELECT * FROM users WHERE username = %s;"
                    for row in self._connection.ask_request(
                            request, (self._username,)):
                        self._id = row["id"]
                        self._family = row["family_name"]
                        self._nick = row["nick_name"]
                except pymysql.err.OperationalError as error:
                    status = "{}\n{}".format(error.args[0], error.args[1])
                    self.status_connection.emit(False, status)
                else:
                    if DEBUG_MODE:
                        print("=====  U S E R  (normal) ======")
                        print("connected to:",
                              self._id, "-", self._nick, "-", self._family)
                    self.status_connection.emit(True, "Vous êtes connecté")

    def new_user_ready(self):
        """When user has been created successfully"""

        self.status_connection.emit(True, "Nouvel utilisateur {} "
                                          "enregistré".format(self._username))

    def disconnect(self):
        """disconnect User to local database"""

        if not self.is_admin() and self.is_connected():
            self._connection.disconnect()
            self.status_connection.emit(False, "Vous êtes déconnecté")

    def is_admin(self):
        """Tell if this user is an Admin connected database server user"""

        return isinstance(self._connection, AdminConnection)

    def is_connected(self):
        """Said if User is connected"""

        return self._connection.is_connected()

    @property
    def connection(self):
        """Database property getter"""

        return self._connection

    @connection.setter
    def connection(self, connection):
        """Database property getter"""

        self._connection = connection

    @property
    def id(self):
        """Return id of user"""

        return self._id

    @property
    def family(self):
        """Return self._family"""

        return self._family

    @property
    def nick(self):
        """Return self._nick"""

        return self._nick

    @property
    def username(self):
        """Return self._username"""

        return self._username
