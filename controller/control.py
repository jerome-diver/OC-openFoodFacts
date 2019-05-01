'''Genral controller for the application'''

from controller import Authentication, DatabaseMode, OpenFoodFactsMode
from view import MainWindow, SignIn, SignUp
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import sys


class Controller(QObject):
    '''Control everything'''

    def __init__(self):
        super().__init__()
        self.app = QApplication([])
        self.window = MainWindow(self)
        self.signin = SignIn(self)
        self.signup = SignUp(self)
        self.window.show()
        sys.exit(self.app.exec_())


    @pyqtSlot()
    def on_quit(self):
        '''Close application slot'''

        self.app.closeAllWindows()

    @pyqtSlot()
    def on_sign_in(self):
        '''Sing-in button slot'''

        self.signin.open()

    @pyqtSlot()
    def on_sign_up(self):
        '''Sing-up button slot'''

        self.signup.open()

    @pyqtSlot()
    def on_local_mode(self):
        '''OpenFoodFacts list button slot'''

        self.window.openfoodfacts_mode.setChecked(False)

    @pyqtSlot()
    def on_openfoodfacts_mode(self):
        '''Local list slot'''

        self.window.local_mode.setChecked(False)