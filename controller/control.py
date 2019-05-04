'''Genral controller for the application'''

from controller import Authentication, DatabaseMode, OpenFoodFactsMode
from view import MainWindow, SignIn, SignUp
from controller import Authentication
from model import Database
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import sys
import pymysql


class Controller(QObject):
    '''Control everything'''

    def __init__(self):
        super().__init__()
        self.app = QApplication([])
        self.authenticate = Authentication()
        self.window = MainWindow(self)
        self.window.show()
        self.db_mode = None
        self.off_mode = None
        self.window.quit.clicked.connect(self.on_quit)
        self.window.signin.clicked.connect(self.authenticate.on_sign_in)
        self.window.signup.clicked.connect(self.authenticate.on_sign_up)
        self.window.openfoodfacts_mode.clicked. \
            connect(self.on_openfoodfacts_mode)
        self.window.local_mode.clicked.connect(self.on_local_mode)
        sys.exit(self.app.exec_())

    @pyqtSlot()
    def on_quit(self):
        '''Close application slot'''

        self.app.closeAllWindows()

    @pyqtSlot()
    def on_local_mode(self):
        '''OpenFoodFacts list button slot'''

        self.window.openfoodfacts_mode.setChecked(False)
        if self.off_mode:
            del self.off_mode
        self.db_mode = DatabaseMode(
            self.window,
            self.authenticate.get_database())

    @pyqtSlot()
    def on_openfoodfacts_mode(self):
        '''Local list slot'''

        self.window.local_mode.setChecked(False)
        if self.db_mode:
            del self.db_mode
        self.off_mode = OpenFoodFactsMode(
            self.window,
            self.authenticate.get_database())
