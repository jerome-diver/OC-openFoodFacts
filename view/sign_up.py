'''Sign-up Qt-5 Dialog view'''

from PyQt5.QtWidgets import QDialog
from ui import Ui_SignUp

class SignUp(QDialog, Ui_SignUp):
    '''Sign up User view'''

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setupUi(self)

