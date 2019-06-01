"""Sign-in Qt-5 Dialog box view"""

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSlot

from ui import Ui_SignIn
from view.mixin import MixinSigns


class SignIn(QDialog, Ui_SignIn, MixinSigns):
    """Sign in User view"""

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.setupUi(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.username.textChanged.connect(self.on_reset_status)
        self.password.textChanged.connect(self.on_reset_status)

    def reset(self):
        """Reset entries"""

        self.password.setText("")
        self.username.setText("")

    @pyqtSlot()
    def on_reset_status(self):
        """Need to share with parent at edit time"""

        super(SignIn, self).on_reset_status()

    @pyqtSlot(str)
    def on_status(self, message):
        """send back to parent"""

        super(SignIn, self).on_status(message)
