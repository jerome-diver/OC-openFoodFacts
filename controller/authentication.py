'''Controller for anthentication of user with local database'''

from model import Database, User
from view import SignUp, SignIn
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPalette
import pymysql

class Authentication(QObject):
    '''Authenticate User on local database'''
    username_exist = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._db = Database()
        self.signin = SignIn(self)
        self.signup = SignUp(self)
        self.signin.cancel.clicked.connect(self.on_close)
        self.signin.connection.clicked.connect(self.connect_user)
        self.signin.username.textChanged.connect(self.signin.on_reset_status)
        self.signin.password.textChanged.connect(self.signin.on_reset_status)
        self.signup.cancel.clicked.connect(self.on_close)
        self.signup.username.textChanged.connect(self.on_username_changed)
        self.signup.password.textChanged.connect(self.signup.on_reset_status)
        self.username_exist.connect(self.signin.on_username_exist)
        self.username_exist.connect(self.signup.on_username_exist)


    @pyqtSlot()
    def on_sign_in(self):
        '''Sing-in button slot'''

        self.signin.open()

    @pyqtSlot()
    def on_sign_up(self):
        '''Sing-up button slot'''

        self.signup.open()

    @pyqtSlot()
    def on_close(self):
        '''Dialog box close slot'''

        self.signin.close()
        self.signup.close()

    @pyqtSlot(str)
    def on_username_changed(self, username):
        print(username)
        if self._db.exist_username(self.signup.username.text()):
            self.signup.status.setStyleSheet("color: red; background-color: "
                                             "rgba(20,20,20,0.7);")
            self.username_exist.emit(username)
        else:
            self.signup.status.setStyleSheet("color: green;")

    def connect_user(self):
        username = self.signin.username.text()
        password = self.signin.password.text()
        try:
            self._db = Database(username, password,
                                'openfoodfacts_substitutes')
        except pymysql.err.OperationalError:
            self.signin.status.setStyleSheet("color: red; background-color: "
                                             "rgba(20,20,20,0.7);")
            self.signin.status.setText("Can not connect, username or "
                                       "password failed")

    def new_user(self):
        username = self.signup.username.text()
        password = self.signup.password.text()
        nick_name = self.signup.nickname.text()
        family_name = self.signup.familyname.text()
        self._db.create_user(username, password)
        if len(username) <= 8:
            self.signup.status_label.setText("this username is too short")
        elif self._db.exist_username(username):
            self.signup.status_label.setText("this username exist already")
        else:
            self._db.record_user(username, nick_name, family_name)
            self.connect_user()
