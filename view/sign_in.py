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
        self._user_has_to_be_create = False
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

    @property
    def user_has_to_be_create(self):
        "Property for user_has_to_be_create"

        return self._user_has_to_be_create

    @user_has_to_be_create.setter
    def user_has_to_be_create(self, value):
        """Setter for user_has_to_be_create"""

        if isinstance(value, bool):
            self._user_has_to_be_create = value
        else:
            raise Exception("user_has_to_be_create has to be a bool value")