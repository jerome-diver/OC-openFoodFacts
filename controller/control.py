"""Genral controller for the application"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from controller import DatabaseMode, OpenFoodFactsMode, \
                       UpdateCategories, Authentication
from model import OpenFoodFacts, User,TypeConnection, AdminConnection
from view import MainWindow
from settings import DEBUG_MODE


class Controller(QObject):
    """Control everything"""

    status_message = pyqtSignal(str)
    user_connected = pyqtSignal(User)
    user_disconnected = pyqtSignal()

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
        self._window.local_mode.setDisabled(True)
        self._window.remove.setDisabled(True)
        off_model = OpenFoodFacts()
        loader = UpdateCategories(self._authenticate.user_connection,
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
        self._window.remove.clicked.connect(self.on_remove_substitutes)
        self.status_message.connect(self._window.on_status_message)
        self._authenticate.status_user_connection.connect(
            self.on_new_status_connection)

    @pyqtSlot()
    def on_quit(self):
        """Close application slot"""

        self._app.closeAllWindows()

    @pyqtSlot()
    def on_sign_in(self):
        """Sign-In / Sign-Out button slot"""

        if self._window.signin.text() == "Sign-in":
            self._authenticate.on_sign_in()
        else:   # Sign-Out
            self._authenticate.user.disconnect()
            self._window.signin.setText("Sign-in")
            self._authenticate.user = None

    @pyqtSlot(TypeConnection)
    def on_new_status_connection(self, connected):
        """When user is connected (or failed to be connected)
         to his local database"""

        self._flags["user_connected"] = connected
        if connected == TypeConnection.USER_CONNECTED:
            self.user_connected.emit(self._authenticate.user)
            self.status_message.emit("L'utilisateur est connecté à "
                                     "la base de donnée locale")
            self._window.signup.setHidden(True)
            self._window.signin.setText("Sign-out {}".format(
                self._authenticate.user.username))
            self._window.user_informations.setText(
                "{} {}".format(self._authenticate.user.family,
                               self._authenticate.user.nick))
            self._window.local_mode.setEnabled(True)
        elif connected == TypeConnection.USER_DISCONNECTED:
            self._authenticate.define_user(AdminConnection())
            self.user_disconnected.emit()
            if self._window.local_mode.isChecked():
                self.on_openfoodfacts_mode(True)
            else:
                self._window.local_mode.setDisabled(True)
            self.status_message.emit("L'utilisateur est déconnecté de la base "
                                     "de donnée locale")
            self._window.signup.setHidden(False)
            self._window.user_informations.setText("")
        elif connected == TypeConnection.ADMIN_CONNECTED:
            if DEBUG_MODE:
                print("=====  C O N T R O L  =====")
                print("get signal ADMIN is connected")
        self.checked_substitutes()

    @pyqtSlot(bool)
    def on_local_mode(self, state):
        """OpenFoodFacts list button slot"""

        self._window.openfoodfacts_mode.setChecked(False)
        self._window.local_mode.setDisabled(True)
        self._window.openfoodfacts_mode.setDisabled(False)
        self._window.reset_views()
        if state:
            self._window.record.setHidden(True)
            if self._off_mode:
                self._off_mode.disconnect_signals()
                self._off_mode = None
            if not self._db_mode:
                self._db_mode = DatabaseMode(self._window,
                                             self._authenticate)
        else:
            self._window.reset_views()

    @pyqtSlot(bool)
    def on_openfoodfacts_mode(self, state):
        """Local list slot"""

        self._window.reset_views()
        self._window.local_mode.setChecked(not state)
        self._window.openfoodfacts_mode.setChecked(state)
        self._window.openfoodfacts_mode.setDisabled(state)
        local_mode_status = self._authenticate.user.is_connected() \
                            and not self._authenticate.user.is_admin()
        self._window.local_mode.setEnabled(local_mode_status)
        self._window.record.setHidden(not state)
        if state:
            if self._db_mode:
                self._db_mode.disconnect_signals()
                self._db_mode = None
            if not self._off_mode:
                self._off_mode = OpenFoodFactsMode(self._window,
                                                   self._authenticate)
                self._off_mode.load_details_finished.connect(
                    self.on_load_details_finished)
                self._off_mode.checked_start.connect(self.on_checked_started)
                self.user_connected.connect(
                    self._off_mode.model.on_user_connected)
                self.user_disconnected.connect(
                    self._off_mode.model.on_user_disconnected)
            else:
                self._window.show_categories(
                    self._off_mode.model.categories)
                self._window.show_foods(self._off_mode.model.foods)
                self._window.show_substitutes(
                    self._off_mode.model.substitutes)
                self._window.show_product_details(
                    self._off_mode.model.product_details)
                self._off_mode.load__details.finished.disconnect(
                    self.on_load_details_finished)
                self._off_mode.checked_start.disconnect(
                    self.on_checked_started)
                self.user_connected.disconnect(
                    self._off_mode.model.on_user_connected)
                self.user_disconnected.disconnect(
                    self._off_mode.model.on_user_disconnected)
        else:
            self._window.reset_views()

    def checked_substitutes(self):
        """When signal reset_substitutes from OpenFoodFactsMode is emit
        button recorded for local database has to be disabled"""

        self._window.record.setEnabled(False)
        self._window.record.setDisabled(True)
        if not self._flags["user_connected"]:
            self._window.record.setText("Aucun utilisateur connecté")
            self._window.remove.setText("Aucun utilisateur connecté")
        elif not self._flags["checked_product"]:
            self._window.record.setText("Aucune sélection de substitut")
            self._window.remove.setText("Aucune sélection de substitut")
        elif not self._flags["checked_details"]:
            self._window.record.setText("Attendez, recherche des détails "
                                        "pour la sélection")
            self._window.remove.setText("Attendez, recherche des détails "
                                        "pour la sélection")
        else:
            self._window.record.setText("Enregistrer dans ma base de donnée")
            self._window.remove.setText("Supprimer de ma base de donnée")
            self._window.record.setEnabled(True)
            self._window.remove.setEnabled(True)

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

    @pyqtSlot()
    def on_record_substitutes(self):
        """Record substitutes selected for product food selected inside
        local database"""

        database = self._authenticate.user_connection
        if database:
            user_id = self._authenticate.user.id
            if DEBUG_MODE:
                print("user id:", user_id)
            ok = database.new_record(
                self._off_mode.model.foods.category_id,
                self._off_mode.model.foods.selected_details,
                self._off_mode.model.product_details.checked,
                user_id)
            if ok:
                self._off_mode.model.substitutes.reset_checkboxes()

    @pyqtSlot()
    def on_remove_substitutes(self):
        """Record substitutes selected for product food selected inside
        local database"""

        database = self._authenticate.user_connection
        if database:
            user_id = self._authenticate.user.id
            if DEBUG_MODE:
                print("user id:", user_id)
            ok = database.del_record(
                self._off_mode.model.foods.selected[0],
                self._off_mode.model.substitutes.checked,
                user_id)
            if ok:
                self._off_mode.model.substitutes.reset_checkboxes()

