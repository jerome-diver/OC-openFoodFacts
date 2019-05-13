'''Genral controller for the application'''

from controller import DatabaseMode, OpenFoodFactsMode
from controller import UpdateCategories
from view import MainWindow
from controller import Authentication
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

import sys
import pymysql


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
        loader = UpdateCategories(self._authenticate.get_database())
        loader.start()
        sys.exit(self._app.exec_())

    def connect_signals(self):
        '''Let's connect signals to slots for concerned controller'''

        self._window.quit.clicked.connect(self.on_quit)
        self._window.signin.clicked.connect(self._authenticate.on_sign_in)
        self._window.signup.clicked.connect(self._authenticate.on_sign_up)
        self._window.openfoodfacts_mode.clicked.connect(
            self.on_openfoodfacts_mode)
        self._window.local_mode.clicked.connect(self.on_local_mode)
        self.status_message.connect(self._window.on_status_message)
        self._authenticate.status_user_connected.connect(
            self.on_user_connected)

    @pyqtSlot()
    def on_quit(self):
        '''Close application slot'''

        self._app.closeAllWindows()

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
            else:
                self._off_mode.on_load_categories_finished()
                self._off_mode.on_load_foods_finished()
                self._off_mode.show_substitutes()
                self._off_mode.on_load_product_details_finished()
        else:
            self._window.reset_views()

    @pyqtSlot()
    def on_user_connected(self):
        '''When user is connected to his local database'''

        pass