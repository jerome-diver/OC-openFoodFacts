"""Controller for authentication of user with local database"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

from model import Database, User
from view import SignUp, SignIn


class Authentication(QObject):
    """authenticate user on local database"""

    status_message = pyqtSignal(str)
    status_user_connection = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._dialog_open = None
        self._db = Database()
        self.initialize_database()
        self._sign_in = SignIn(self)
        self._sign_up = SignUp(self)
        self._user = User()
        self.connect_signals()

    @property
    def user(self):
        """self._user getter property"""

        return self._user

    @user.setter
    def user(self, value):
        """User setter property access"""

        self._user = value

    def initialize_database(self):
        """Initialization of Open Food Facts database"""

        self._db.generate_database()
        self._db.generate_users_role()
        self._db.connect_to_off_db()

    def connect_signals(self):
        """Let's connect signals to slots for concerned controller"""

        self._sign_in.cancel.clicked.connect(self.on_close)
        self._sign_in.connection.clicked.connect(self.connect_user)
        self._sign_in.username.textChanged.connect(self._sign_in.on_reset_status)
        self._sign_in.password.textChanged.connect(self._sign_in.on_reset_status)
        self._sign_up.cancel.clicked.connect(self.on_close)
        self._sign_up.username.textChanged.connect(self.on_username_changed)
        self._sign_up.record.clicked.connect(self.new_user)
        self.status_message.connect(self._sign_in.on_status)
        self.status_message.connect(self._sign_up.on_status)
        self._user.status_connected.connect(self.on_connection_return)

    #@pyqtSlot()
    def on_sign_in(self):
        """Sing-in button slot"""

        self._sign_in.open()
        self._dialog_open = "SignIn"

    @pyqtSlot()
    def on_sign_up(self):
        """Sing-up button slot"""

        self._sign_up.open()
        self._dialog_open = "_sign_up"

    @pyqtSlot()
    def on_close(self):
        """Dialog box close slot"""

        if self._dialog_open == "SignIn":
            self._sign_in.close()
        if self._dialog_open == "_sign_up":
            self._sign_up.close()
        self._dialog_open = None

    @pyqtSlot(bool, str)
    def on_connection_return(self, connected, status):
        """Slot for connection action after signal emited"""

        if connected:
            QMessageBox.information(None, "Connexion réussie", status)
            self.on_close()
        else:
            self._sign_in.status.setText("Username or password failed")
            QMessageBox.information(None, "Problème de connexion", status)
        self.status_user_connection.emit(connected)


    @pyqtSlot(str)
    def on_username_changed(self, username):
        """Slot action when username text is changed"""

        if self._db.exist_username(self._sign_up.username.text()):
            self.status_message.emit("{} exite déjà".format(username))
        else:
            self._sign_up.on_reset_status()

    def connect_user(self):
        """Do connect the user"""

        username = self._sign_in.username.text()
        password = self._sign_in.password.text()
        self._user.connect(username, password)

    def new_user(self):
        """Create a new user"""

        username = self._sign_up.username.text()
        password = self._sign_up.password.text()
        nick_name = self._sign_up.nickname.text()
        family_name = self._sign_up.familyname.text()
        if len(username) <= 6:
            self.status_message.emit("Nom d'utilisateur trop court "
                                     "(+ de 8 lettres)")
        elif self._db.exist_username(username):
            self.status_message.emit("{} exite déjà".format(username))
        else:
            self._db.create_user(username, password)
            self._db.record_user(username, nick_name, family_name)

    def get_database(self):
        """Return the super admin database instance"""

        return self._db

    def get_user_database(self):
        """Return the user database"""

        return self._user.database
