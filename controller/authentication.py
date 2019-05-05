'''Controller for anthentication of user with local database'''

from model import Database, User
from view import SignUp, SignIn
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
import pymysql

class Authentication(QObject):
    '''Authenticate User on local database'''
    status_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.dialog_open = None
        self._db = Database()
        self.signin = SignIn(self)
        self.signup = SignUp(self)
        self.connect_signals()

    def connect_signals(self):
        '''Let's connect signals to slots for concerned controller'''

        self.signin.cancel.clicked.connect(self.on_close)
        self.signin.connection.clicked.connect(self.connect_user)
        self.signin.username.textChanged.connect(self.signin.on_reset_status)
        self.signin.password.textChanged.connect(self.signin.on_reset_status)
        self.signup.cancel.clicked.connect(self.on_close)
        self.signup.username.textChanged.connect(self.on_username_changed)
        self.signup.record.clicked.connect(self.new_user)
        self.status_message.connect(self.signin.on_status)
        self.status_message.connect(self.signup.on_status)


    @pyqtSlot()
    def on_sign_in(self):
        '''Sing-in button slot'''

        self.signin.open()
        self.dialog_open = "SignIn"

    @pyqtSlot()
    def on_sign_up(self):
        '''Sing-up button slot'''

        self.signup.open()
        self.dialog_open = "SignUp"

    @pyqtSlot()
    def on_close(self):
        '''Dialog box close slot'''

        if self.dialog_open == "SignIn":
            self.signin.close()
        if self.dialog_open == "SignUp":
            self.signup.close()
        self.dialog_open = None

    @pyqtSlot(str)
    def on_username_changed(self, username):
        if self._db.exist_username(self.signup.username.text()):
            self.status_message.emit("{} exite déjà".format(username))
        else:
            self.signup.on_reset_status()

    def connect_user(self):
        username = self.signin.username.text() if self.dialog_open == "SignIn"\
                        else self.signup.username.text()
        password = self.signin.password.text() if self.dialog_open == "SignIn"\
                        else self.signup.password.text()
        try:
            self._db = Database(username, password, 'openfoodfacts_substitutes')
            QMessageBox.information(None, "Connexion réussie",
                                    "Vous êtes connecté à vôtre base de "
                                    "donnée")
            self.on_close()
        except pymysql.err.OperationalError as e:
            self.signin.status.setText("Username or password failed")
            QMessageBox.information(None, "Problème de connexion",
                                    "{}\n{}".format(e.args[0], e.args[1]))

    def new_user(self):
        username = self.signup.username.text()
        password = self.signup.password.text()
        nick_name = self.signup.nickname.text()
        family_name = self.signup.familyname.text()
        if len(username) <= 8:
            self.status_message.emit("Nom d'utilisateur trop court "
                                       "(+ de 8 lettres)")
        elif self._db.exist_username(username):
            self.status_message.emit("{} exite déjà".format(username))
        else:
            self._db.create_user(username, password)
            self._db.record_user(username, nick_name, family_name)
            self.connect_user()

    def get_database(self):
        return self._db