'''Genral controller for the application'''

from controller import Authentication, DatabaseMode, OpenFoodFactsMode
from view import MainWindow, SignIn, SignUp
from controller import Authentication
from model import Database
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

import sys
import pymysql


class Controller(QObject):
    '''Control everything'''

    status_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.app = QApplication([])
        self.authenticate = Authentication()
        self.window = MainWindow(self)
        self.window.show()
        self.db_mode = None
        self.off_mode = None
        self.connect_signals()
        sys.exit(self.app.exec_())

    def connect_signals(self):
        '''Let's connect signals to slots for concerned controller'''

        self.window.quit.clicked.connect(self.on_quit)
        self.window.signin.clicked.connect(self.authenticate.on_sign_in)
        self.window.signup.clicked.connect(self.authenticate.on_sign_up)
        self.window.openfoodfacts_mode.clicked.connect(
            self.on_openfoodfacts_mode)
        self.window.local_mode.clicked.connect(self.on_local_mode)
        self.status_message.connect(self.window.on_status_message)

    @pyqtSlot()
    def on_quit(self):
        '''Close application slot'''

        self.app.closeAllWindows()

    @pyqtSlot(bool)
    def on_local_mode(self, state):
        '''OpenFoodFacts list button slot'''

        self.window.openfoodfacts_mode.setChecked(False)
        if state:
            if self.off_mode:
                self.off_mode = None
            if not self.db_mode:
                self.db_mode = DatabaseMode(
                    self.window,
                    self.authenticate.get_database())
        else:
            self.window.reset_views()

    @pyqtSlot(bool)
    def on_openfoodfacts_mode(self, state):
        '''Local list slot'''

        if state:
            self.window.local_mode.setChecked(False)
            if self.db_mode:
                del self.db_mode
            if not self.off_mode:
                self.off_mode = OpenFoodFactsMode(
                    self.window,
                    self.authenticate.get_database())
            else:
                self.off_mode.on_load_categories_finished()
                self.off_mode.on_load_foods_finished()
                self.off_mode.show_substitutes()
                self.off_mode.on_load_product_details_finished()
        else:
            self.window.reset_views()
