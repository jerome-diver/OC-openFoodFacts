'''Genral controller for the application'''

from controller import Authentication, DatabaseMode, OpenFoodFactsMode
from view import MainWindow
from PyQt5.QtWidgets import QApplication, QtCore, \
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import sys


class Controller(QObject):
    '''Control everything'''

    def __init__(self):
        app = QApplication([])
        window = MainWindow(self)
        window.show()
        sys.exit(app.exec_())


    @pyqtSlot()
    def on_quit(self):
        pass
