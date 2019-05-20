"""Genral controller for the application"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from controller import DatabaseMode, OpenFoodFactsMode, \
                       UpdateCategories, Authentication
from model import OpenFoodFacts
from view import MainWindow
from settings import DEBUG_MODE


class Controller(QObject):
    """Control everything"""

    status_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._app = QApplication([])
        self._authenticate = Authentication()
        self._window = MainWindow(self)
        self._window.show()
        self._db_mode = None
        self._off_mode = None
        self._flags = dict(user_connected=False,
                           checked_product=False,
                           checked_details=False)
        self.connect_signals()
        off_model = OpenFoodFacts()
        loader = UpdateCategories(self._authenticate.get_database(),
                                  off_model)
        loader.start()
        self.checked_substitutes()
        sys.exit(self._app.exec_())

    def connect_signals(self):
        """Let's connect signals to slots for concerned controller"""

        self._window.quit.clicked.connect(self.on_quit)
        self._window.signin.clicked.connect(self.on_sign_in)
        self._window.signup.clicked.connect(self._authenticate.on_sign_up)
        self._window.openfoodfacts_mode.clicked.connect(
            self.on_openfoodfacts_mode)
        self._window.local_mode.clicked.connect(self.on_local_mode)
        self._window.record.clicked.connect(self.on_record_substitutes)
        self.status_message.connect(self._window.on_status_message)
        self._authenticate.status_user_connection.connect(
            self.on_user_connection)

    @pyqtSlot()
    def on_quit(self):
        """Close application slot"""

        self._app.closeAllWindows()

    @pyqtSlot()
    def on_sign_in(self):
        """Sing-in button slot"""

        if self._window.signin.text() == "Sign-in":
            self._authenticate.on_sign_in()
        else:
            self._authenticate.user.disconnect()
            self.status_message.emit("Utilisateur {} {} déconnecté".
                                     format(self._authenticate.user.family,
                                            self._authenticate.user.nick))
            self._window.signin.setText("Sign-in")

    @pyqtSlot(bool)
    def on_local_mode(self, state):
        """OpenFoodFacts list button slot"""

        self._window.openfoodfacts_mode.setChecked(False)
        if state:
            if self._off_mode:
                self._off_mode.disconnect_signals()
                self._window.reset_views()
                self._off_mode = None
            if not self._db_mode:
                self._db_mode = DatabaseMode(
                    self._window,
                    self._authenticate.get_database())
        else:
            self._window.reset_views()

    @pyqtSlot(bool)
    def on_openfoodfacts_mode(self, state):
        """Local list slot"""

        if state:
            self._window.local_mode.setChecked(False)
            if self._db_mode:
                self._db_mode.disconnect_signals()
                self._db_mode = None
            if not self._off_mode:
                self._off_mode = OpenFoodFactsMode(
                    self._window,
                    self._authenticate.get_database())
                self._off_mode.load_details_finished.connect(
                    self.on_load_details_finished)
                self._off_mode.checked_start.connect(self.on_checked_started)
            else:
                self._window.show_categories()
                self._window.show_foods()
                self._window.show_substitutes()
                self._window.show_product_details()
                self._off_mode.load__details.finished.disconnect(
                    self.on_load_details_finished)
                self._off_mode.checked_start.disconnect(
                    self.on_checked_started)
        else:
            self._window.reset_views()

    def checked_substitutes(self):
        """When signal reset_substitutes from OpenFoodFactsMode is emit
        button recorded for local database has to be disabled"""

        self._window.record.setEnabled(False)
        self._window.record.setDisabled(True)
        if not self._flags["user_connected"]:
            self._window.record.setText("Aucun utilisateur connecté")
        elif not self._flags["checked_product"]:
            self._window.record.setText("Aucune sélection de substitut")
        elif not self._flags["checked_details"]:
            self._window.record.setText("Attendez, recherche des détails "
                                        "pour la sélection")
        else:
            self._window.record.setText("Enregistrer dans la base de donnée")
            self._window.record.setEnabled(True)

    @pyqtSlot()
    def on_load_details_finished(self):
        """When product substitutes checked details are loaded..."""

        if self._off_mode:
            self._flags["checked_product"] = bool(
                self._off_mode.model.substitutes.checked)
            self._flags["checked_details"] = bool(
                self._off_mode.model.product_details.checked)
        self.checked_substitutes()

    @pyqtSlot()
    def on_checked_started(self):
        """Slot for receipt signal to said if substitutes list any selection"""

        self._flags["checked_product"] = True
        self._flags["checked_details"] = False
        self.checked_substitutes()

    @pyqtSlot(bool)
    def on_user_connection(self, connected):
        """When user is connected to his local database"""

        self._flags["user_connected"] = connected
        if connected:
            self.status_message.emit("L'utilisateur est connecté à "
                                 "la base de donnée locale")
            self._window.signin.setText("Sign-out")
        else:
            self.status_message.emit("L'utilisateur est déconnecté de la base "
                                     "de donnée locale")
            self._window.signin.setText("Sign-in")
        self.checked_substitutes()

    @pyqtSlot()
    def on_record_substitutes(self):
        """Record substitutes selected for product food selected inside
        local database"""

        database = self._authenticate.get_user_database()
        if database:
            user_id = self._authenticate.user.id
            if DEBUG_MODE:
                print("user id:", user_id)
            database.new_record(self._off_mode.model.categories.selected,
                                self._off_mode.model.foods.selected,
                                self._off_mode.model.substitutes.checked,
                                self._off_mode.model.product_details.checked,
                                user_id)

