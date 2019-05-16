'''Controller for authentication of user with local database'''

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

from model import Database, User
from view import SignUp, SignIn

class Authentication(QObject):
    '''Authenticate User on local database'''

    status_message = pyqtSignal(str)
    status_user_connected = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.dialog_open = None
        self._db = Database()
        self.initialize_database()
        self.signin = SignIn(self)
        self.signup = SignUp(self)
        self._user = User()
        self.connect_signals()

    @property
    def user(self):
        '''self._user getter property'''

        return self._user


    def initialize_database(self):
        '''Initialization of Open Food Facts database'''

        self._db.generate_database()
        self._db.generate_users_role()
        self._db.connect_to_off_db()

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
        self._user.status_connected.connect(self.on_connection_return)

    #@pyqtSlot()
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

    @pyqtSlot(bool, str)
    def on_connection_return(self, connected, status):
        '''Slot for connection action after signal emited'''

        if connected:
            QMessageBox.information(None, "Connexion réussie", status)
            self.on_close()
            self.status_user_connected.emit()
        else:
            self.signin.status.setText("Username or password failed")
            QMessageBox.information(None, "Problème de connexion", status)


    @pyqtSlot(str)
    def on_username_changed(self, username):
        '''Slot action when username text is changed'''

        if self._db.exist_username(self.signup.username.text()):
            self.status_message.emit("{} exite déjà".format(username))
        else:
            self.signup.on_reset_status()

    def connect_user(self):
        '''Do connect the user'''

        username = self.signin.username.text()
        password = self.signin.password.text()
        self._user.connect(username, password)

    def new_user(self):
        '''Create a new user'''

        username = self.signup.username.text()
        password = self.signup.password.text()
        nick_name = self.signup.nickname.text()
        family_name = self.signup.familyname.text()
        if len(username) <= 6:
            self.status_message.emit("Nom d'utilisateur trop court "
                                     "(+ de 8 lettres)")
        elif self._db.exist_username(username):
            self.status_message.emit("{} exite déjà".format(username))
        else:
            self._db.create_user(username, password)
            self._db.record_user(username, nick_name, family_name)

    def get_database(self):
        '''Return the super admin database instance'''

        return self._db

    def get_user_database(self):
        '''Return the user database'''

        return self._user.database
