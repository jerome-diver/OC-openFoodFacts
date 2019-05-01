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
        sys.exit(self.app.exec_())

    @pyqtSlot()
    def on_quit(self):
        '''Close application slot'''

        self.app.closeAllWindows()

    @pyqtSlot()
    def on_local_mode(self):
        '''OpenFoodFacts list button slot'''

        self.window.openfoodfacts_mode.setChecked(False)

    @pyqtSlot()
    def on_openfoodfacts_mode(self):
        '''Local list slot'''

        self.window.local_mode.setChecked(False)