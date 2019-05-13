'''Sign-up Qt-5 Dialog view'''

from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from ui import Ui_SignUp
from view.share_methods import Share

class SignUp(QDialog, Ui_SignUp, Share):
    '''Sign up User view'''

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setupUi(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.passwd_confirm.setEchoMode(QLineEdit.Password)

    @pyqtSlot()
    def on_reset_status(self):
        '''call superclass slot from Share'''

        super(SignUp, self).on_reset_status()

    @pyqtSlot(str)
    def on_status(self, message):
        '''call superclass slot from Share'''

        super(SignUp, self).on_status(message)
