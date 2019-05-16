'''Genral controller for the application'''

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from controller import DatabaseMode, OpenFoodFactsMode, \
                       UpdateCategories, Authentication
from view import MainWindow

class Controller(QObject):
    '''Control everything'''

    status_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._app = QApplication([])
        self._authenticate = Authentication()
        self._window = MainWindow(self)
        self._window.show()
        self._db_mode = None
        self._off_mode = None
        self.connect_signals()
        loader = UpdateCategories(self._authenticate.get_database(),
                                  self._window)
        loader.start()
        sys.exit(self._app.exec_())

    def connect_signals(self):
        '''Let's connect signals to slots for concerned controller'''

        self._window.quit.clicked.connect(self.on_quit)
        self._window.signin.clicked.connect(self.on_sign_in)
        self._window.signup.clicked.connect(self._authenticate.on_sign_up)
        self._window.openfoodfacts_mode.clicked.connect(
            self.on_openfoodfacts_mode)
        self._window.local_mode.clicked.connect(self.on_local_mode)
        self._window.record.clicked.connect(
            self.on_record_substitutes)
        self.status_message.connect(self._window.on_status_message)
        self._authenticate.status_user_connected.connect(
            self.on_user_connected)

    @pyqtSlot()
    def on_quit(self):
        '''Close application slot'''

        self._app.closeAllWindows()

    @pyqtSlot()
    def on_sign_in(self):
        '''Sing-in button slot'''

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
        '''OpenFoodFacts list button slot'''

        self._window.openfoodfacts_mode.setChecked(False)
        if state:
            if self._off_mode:
                self._off_mode = None
            if not self._db_mode:
                self._db_mode = DatabaseMode(
                    self._window,
                    self._authenticate.get_database())
        else:
            self._window.reset_views()

    @pyqtSlot(bool)
    def on_openfoodfacts_mode(self, state):
        '''Local list slot'''

        if state:
            self._window.local_mode.setChecked(False)
            if self._db_mode:
                self._db_mode = None
            if not self._off_mode:
                self._off_mode = OpenFoodFactsMode(
                    self._window,
                    self._authenticate.get_database())
                self._off_mode.checked_substitutes_event.connect(
                    self.on_checked_substitutes)
                self._off_mode.load_product_details.finished.connect(
                    self.on_load_details_finished)
            else:
                self._off_mode.on_load_categories_finished()
                self._off_mode.on_load_foods_finished()
                self._off_mode.show_substitutes()
                self._off_mode.on_load_product_details_finished()
                self._off_mode.checked_substitutes_event.disconnect(
                    self.on_checked_substitutes)
                self._off_mode.load_product_details.finished.disconnect(
                    self.on_load_details_finished)
        else:
            self._window.reset_views()

    @pyqtSlot()
    def on_user_connected(self):
        '''When user is connected to his local database'''

        self.status_message.emit("L'utilisateur est connecté à "
                                 "la base de donnée locale")
        if self._off_mode:
            self.on_checked_substitutes(bool(self._off_mode.
                                             model.
                                             selected_substitutes))
        self._window.signin.setText("SignOut")

    @pyqtSlot(bool)
    def on_checked_substitutes(self, state):
        '''When signal reset_substitutes from OpenFoodFactsMode is emit
        button recorded for local database has to be disabled'''

        disable = not (bool(self._authenticate.user.connected) and state)
        if self._off_mode.load_product_details.isFinished():
            self._window.record.setText("Enregistrer")
            self._window.record.setDisabled(disable)
        elif not disable:
            self._window.record.setText("Téléchargement des "
                                        "produits sélectionnés")

    @pyqtSlot()
    def on_record_substitutes(self):
        '''Record substitutes selected for product food selected inside
        local database'''

        pass

    @pyqtSlot()
    def on_load_details_finished(self):
        '''When product substitutes checked details are loaded...'''

        self.on_checked_substitutes(True)
