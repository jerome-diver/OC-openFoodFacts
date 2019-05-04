'''Mainwindow Qt-5 application'''

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
from ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    '''Main Window application''' 

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setupUi(self)
        self.openfoodfacts_mode.setChecked(False)
        self.local_mode.setChecked(False)

    def show_categories(self, model):
        self.categories_list.setModel(model)
        self.categories_list.show()
