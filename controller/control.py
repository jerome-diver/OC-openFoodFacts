"""General controller for the application"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from controller import DatabaseMode, OpenFoodFactsMode, \
                       UpdateCategories, Authentication
from model import OpenFoodFacts, User
from enumerator import TypeConnection
from view import MainWindow
from settings import DEBUG_MODE


class Controller(QObject):
    """Control everything"""

    status_message = pyqtSignal(str)
    user_event = pyqtSignal(User)

    def __init__(self):
        super().__init__()
        self._app = QApplication([])
        self._authenticate = Authentication()
        self._window = MainWindow()
        self._window.show()
        self._current_mode = None
        self._flags = dict(user_connected=False,
                           checked_product=False,
                           checked_details=False,
                           end_tasks=False)
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
            self._authenticate.disconnect_user()
            self._window.signin.setText("Sign-in")

    @pyqtSlot(TypeConnection)
    def on_new_status_connection(self, connected):
        """When user is connected (or failed to be connected)
         to his local database"""

        self.user_event.emit(self._authenticate.user)
        self._flags["user_connected"] = connected
        if connected == TypeConnection.USER_CONNECTED:
            self.status_message.emit("L'utilisateur est connecté à "
                                     "la base de donnée locale")
            self._window.signup.setHidden(True)
            self._window.signin.setText("Sign-out {}".format(
                self._authenticate.user.username))
            self._window.user_informations.setText(
                "{} {}".format(self._authenticate.user.family,
                               self._authenticate.user.nick))
            self._window.local_mode.setEnabled(True)
            self._authenticate.user.connection.status_message.connect(
                self._window.on_status_message)
        elif connected == TypeConnection.USER_DISCONNECTED:
            self.status_message.emit("L'utilisateur est déconnecté de la base "
                                     "de donnée locale")
            self._window.signup.setHidden(False)
            self._window.user_informations.setText("")
            self._authenticate.user.connection.status_message.disconnect(
                self._window.on_status_message)
        elif connected == TypeConnection.ADMIN_CONNECTED:
            if self._window.local_mode.isChecked():
                self.on_openfoodfacts_mode(True)
            self._window.local_mode.setDisabled(True)
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
        user_status = self._authenticate.user.is_connected() \
            and not self._authenticate.user.is_admin()
        self._window.record.setHidden(state)
        self._window.remove.setHidden(not state)
        if state:
            self._authenticate.user.connection.connect_to_off_db(
                self._authenticate.user.is_admin())
            if isinstance(self._current_mode, OpenFoodFactsMode):
                self._current_mode.disconnect()
                self._current_mode = None
            if not self._current_mode:
                self._current_mode = DatabaseMode(general_ctrl=self)
                if user_status:
                    self.user_event.emit(self._authenticate.user)
        else:
            self._window.reset_views()

    @pyqtSlot(bool)
    def on_openfoodfacts_mode(self, state):
        """Local list slot"""

        self._window.reset_views()
        self._window.local_mode.setChecked(not state)
        self._window.openfoodfacts_mode.setChecked(state)
        self._window.openfoodfacts_mode.setDisabled(state)
        user_status = self._authenticate.user.is_connected() \
            and not self._authenticate.user.is_admin()
        self._window.local_mode.setEnabled(user_status)
        self._window.record.setHidden(not state)
        self._window.remove.setHidden(state)
        if state:
            self._authenticate.user.connection.connect_to_off_db(
                self._authenticate.user.is_admin())
            if isinstance(self._current_mode, DatabaseMode):
                self._current_mode.disconnect()
                self._current_mode = None
            if not self._current_mode:
                self._current_mode = OpenFoodFactsMode(general_ctrl=self)
                if user_status:
                    self.user_event.emit(self._authenticate.user)
            else :
                self._window.show_categories(
                    self._current_mode.model.categories)
                self._window.show_foods(self._current_mode.model.foods)
                self._window.show_substitutes(
                    self._current_mode.model.substitutes)
                self._window.show_product_details(
                    self._current_mode.model.product_details)
        else:
            self._window.reset_views()

    def checked_substitutes(self):
        """When signal reset_substitutes from OpenFoodFactsMode is emit
        button recorded for local database has to be disabled"""

        self._window.record.setEnabled(False)
        self._window.remove.setEnabled(False)
        if self._flags["user_connected"] != TypeConnection.USER_CONNECTED:
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
        elif not self._flags["end_tasks"]:
            self._window.record.setText(("Recherches en cours..."))
            self._window.remove.setText(("Recherches en cours..."))
        else:
            self._window.record.setText("Enregistrer dans ma base de donnée")
            self._window.remove.setText("Supprimer de ma base de donnée")
            self._window.record.setEnabled(True)
            self._window.remove.setEnabled(True)

    def on_load_details_finished(self):
        """When product substitutes checked details are loaded..."""

        self._flags["checked_product"] = bool(
            self._current_mode.model.substitutes.checked)
        self._flags["checked_details"] = bool(
            self._current_mode.model.product_details.checked)
        self._flags["end_tasks"] = bool(
            len(self._current_mode.model.substitutes.checked) ==
            len(self._current_mode.model.product_details.checked))
        self.checked_substitutes()

    @pyqtSlot()
    def on_checked_started(self):
        """Slot for receipt signal to said if substitutes list any selection"""

        self._flags["checked_product"] = True
        if isinstance(self._current_mode, OpenFoodFactsMode):
            self._flags["checked_details"] = False
        elif isinstance(self._current_mode, DatabaseMode):
            self._flags["checked_details"] = True
        self.checked_substitutes()

    @pyqtSlot()
    def on_record_substitutes(self):
        """Record substitutes selected for product food selected inside
        local database"""

        database = self._authenticate.user_connection
        if database:
            user_id = self._authenticate.user.id
            if DEBUG_MODE:
                print("=====  C O N T R O L  =====")
                print("record substitute(s) for user id:", user_id)
            ok = database.new_record(
                self._current_mode.model.foods.category_id,
                self._current_mode.model.foods.selected_details,
                self._current_mode.model.product_details.checked,
                user_id)
            if ok:
                self.status_message.emit("Substituts enregistrés dans la base "
                                         "de donnée")
                self._refresh_views()

    @pyqtSlot()
    def on_remove_substitutes(self):
        """Record substitutes selected for product food selected inside
        local database"""

        database = self._authenticate.user_connection
        if database:
            user_id = self._authenticate.user.id
            if DEBUG_MODE:
                print("=====  C O N T R O L  =====")
                print("remove substitute(s) for user id:", user_id)
            removed = database.del_record(
                self._current_mode.model.foods.selected[0],
                self._current_mode.model.substitutes.checked,
                user_id)
            if removed:
                self.status_message.emit("Substituts sélectionnés supprimés de "
                                         "la base de données")
            else:
                self.status_message.emit("La suppression des substituts n'a "
                                         "pas fonctionner correctement")
            self._refresh_views()

    def _refresh_views(self):
        """Refresh all views for concerned mode's running"""

        self._current_mode.model.reset_models()
        self._window.reset_views()
        self._current_mode.initialize()

    @property
    def window(self):
        """Property for _window Ui View"""

        return self._window

    @property
    def authenticate(self):
        """Property for authenticate controller"""

        return self._authenticate

    @property
    def views(self):
        """Property for views dict of QWidgets views"""

        return self._views
