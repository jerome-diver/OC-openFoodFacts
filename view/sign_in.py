'''Sign-in Qt-5 Dialog box view'''

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLineEdit
from ui import Ui_SignIn
from view.share_methods import Share

class SignIn(QDialog, Ui_SignIn, Share):
    '''Sign in User view'''

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setupUi(self)
        self.password.setEchoMode(QLineEdit.Password)

    @pyqtSlot()
    def on_reset_status(self):
        '''call superclass slot from Share'''

        super(SignIn, self).on_reset_status()

    @pyqtSlot(str)
    def on_status(self, message):
        '''call superclass slot from Share'''

        super(SignIn, self).on_status(message)