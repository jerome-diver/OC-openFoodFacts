'''Sign-in Qt-5 Dialog box view'''

from PyQt5.QtWidgets import QDialog
from ui import Ui_SignIn

class SignIn(QDialog, Ui_SignIn):
    '''Sign in User view'''

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setupUi(self)
