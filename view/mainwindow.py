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
        self.quit.clicked.connect(self.controller.on_quit)
        self.signin.clicked.connect(self.controller.authenticate.on_sign_in)
        self.signup.clicked.connect(self.controller.authenticate.on_sign_up)
        self.openfoodfacts_mode.clicked.\
             connect(self.controller.on_openfoodfacts_mode)
        self.local_mode.clicked.connect(self.controller.on_local_mode)

