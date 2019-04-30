'''Mainwindow Qt-5 application'''

from PyQt5.QtWidgets import QMainWindow
from ui.ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):
    '''Main Window application''' 

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        ui = Ui_MainWindow()
        ui.setupUi(self)

