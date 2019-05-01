'''Sign-in Qt-5 Dialog box view'''

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from ui import Ui_SignIn

class SignIn(QDialog, Ui_SignIn):
    '''Sign in User view'''

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setupUi(self)

    @pyqtSlot(str)
    def on_username_exist(self, username):
        '''Should emit a signal with arguments:
        username, nick_name, family_name'''

        self.status.setText("username {} exist already".format(username))

    @pyqtSlot()
    def on_reset_status(self):
        self.status.setText("")
        self.status.setStyleSheet("background-color: rgba(0,0,0,0);")