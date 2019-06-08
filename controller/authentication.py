"""Controller for authentication of user with local database"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from time import sleep

from enumerator import TypeConnection
from model import DatabaseConnection, AdminConnection, \
                  UserConnection, User
from view import SignUp, SignIn


class Authentication(QObject):
    """authenticate user on local database"""

    status_message = pyqtSignal(str)
    status_user_connection = pyqtSignal(TypeConnection)

    def __init__(self):
        super().__init__()
        self._dialog_open = None
        self._dialog_count = 0
        self._user = None
        self.define_user(AdminConnection())
        self.initialize_database()
        self._sign_in = SignIn()
        self._sign_up = SignUp()
        self.connect_signals()

    def define_user(self, type):
        """Define user and connect"""

        if self._user:
            if isinstance(self._user, User):
                self._user.status_connection.disconnect(
                    self.on_new_status_connection)
        if isinstance(type, DatabaseConnection):
            self._user = User(type)
           # if isinstance(type, AdminConnection):
        elif isinstance(type, User):
            self._user = type
        self._user.status_connection.connect(self.on_new_status_connection)

    def initialize_database(self):
        """Initialization of Open Food Facts database"""

        _admin_connection = self._user.connection
        _admin_connection.generate_database()
        _admin_connection.generate_users_role()

    def connect_signals(self):
        """Let's connect signals to slots for concerned controller"""

        self._sign_in.connection.clicked.connect(self.connect_user)
        self._sign_in.cancel.clicked.connect(self.on_close)
        self._sign_up.username.textChanged.connect(self.on_username_changed)
        self._sign_up.record.clicked.connect(self.new_user)
        self._sign_up.cancel.clicked.connect(self.on_close)
        self.status_message.connect(self._sign_in.on_status)
        self.status_message.connect(self._sign_up.on_status)

    #@pyqtSlot()
    def on_sign_in(self):
        """Sing-in button call from controller"""

        self._sign_in.reset()
        self._dialog_open = "SignIn"
        self._sign_in.open()

    @pyqtSlot()
    def on_sign_up(self):
        """Sing-up button slot"""

        self._sign_up.reset()
        self._dialog_open = "SignUp"
        self._sign_up.open()

    @pyqtSlot()
    def on_close(self):
        """Dialog box close slot"""

        if self._dialog_open == "SignIn" and \
             not self._sign_in.user_has_to_be_create:
            self._sign_in.close()
        elif self._dialog_open == "SignUp":
            self._sign_up.close()
            if self._sign_in.user_has_to_be_create:
                self._sign_in.user_has_to_be_create = False
                self._sign_up.user_create = False

    @pyqtSlot(bool, str)
    def on_new_status_connection(self, connected, status):
        """Slot for connection action after signal emited"""

        if connected:
            QMessageBox.information(None, "Connexion réussie", status)
            self.on_close()
            self.status_user_connection.emit(TypeConnection.USER_CONNECTED)
        else:
            self._sign_in.status.setText("Username or password failed")
            QMessageBox.information(None, "Problème de connexion", status)
            self.status_user_connection.emit(TypeConnection.USER_DISCONNECTED)

    @pyqtSlot(str)
    def on_username_changed(self, username):
        """Slot action when username text is changed"""

        if self._user.connection.exist_username(
                self._sign_up.username.text()):
            self.status_message.emit("{} exite déjà".format(username))
        else:
            self._sign_up.on_reset_status()

    def connect_user(self):
        """Do connect the user"""

        username = self._sign_in.username.text()
        password = self._sign_in.password.text()
        if self._user.connection.can_connect(username, password):
            if not self._user.connection.exist_username(username):
                self.status_message.emit(
                    "l'utilisateur est inconnu de la base locale")
                self._sign_in.user_has_to_be_create = True
                self._sign_up.user_create = True
                self.on_sign_up()
                self._sign_up.set_exist_username(username=username,
                                                 password=password)
            else:
                self._sign_in.user_has_to_be_create = False
                self._sign_up.user_create = False
                self.define_user(UserConnection())
                self._user.connect(username, password)
        else:
            self.status_message.emit("Cet utilisateur ne peut pas accéder à "
                                     "la base de donnée")

    def disconnect_user(self):
        """Disconnect current user and change to AdminConnection
        GRANT user"""

        self._user.disconnect()
        self.define_user(AdminConnection())
        if self._user.connection.is_connected():
            self.status_user_connection.emit(TypeConnection.ADMIN_CONNECTED)

    def new_user(self):
        """Create a new user"""

        username = self._sign_up.username.text()
        password = self._sign_up.password.text()
        nick_name = self._sign_up.nickname.text()
        family_name = self._sign_up.familyname.text()
        confirm_passwd = self._sign_up.passwd_confirm.text()
        if len(username) <= 6:
            self.status_message.emit("Nom d'utilisateur trop court "
                                     "(+ de 8 lettres)")
        elif self._user.connection.exist_username(username):
            self.status_message.emit("{} exite déjà".format(username))
        elif password != confirm_passwd:
            self.status_message.emit(
                "Les mots de passe ne correspondent pas")
        else:
            try:
                self._user.connection.create_user(username, password)
                self._user.connection.record_user(
                    username, nick_name, family_name)
            except:
                set.status_message.emit("Problème lors de l'enregstrement")
            else:
                self.status_message.emit("Utilisateur enregistré")
                self.user.new_user_ready()
                self._sign_up.user_create = False
                self.on_close()

    @property
    def user_connection(self):
        """Return the user database"""

        return self._user.connection

    @property
    def user(self):
        """self._user getter property"""

        return self._user

    @user.setter
    def user(self, usr):
        """User setter property access"""

        self.define_user(usr)
