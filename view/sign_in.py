"""Sign-in Qt-5 Dialog box view"""

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLineEdit
from ui import Ui_SignIn
from view.mixin import MixinSigns


class SignIn(QDialog, Ui_SignIn, MixinSigns):
    """Sign in User view"""

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.setupUi(self)
        self.password.setEchoMode(QLineEdit.Password)

    def reset(self):
        """Reset entries"""

        self.password.setText("")
        self.username.setText("")