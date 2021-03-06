"""Sign-up Qt-5 Dialog view"""

from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtCore import pyqtSlot

from ui import Ui_SignUp
from view.mixin import MixinSigns


class SignUp(QDialog, Ui_SignUp, MixinSigns):
    """Sign up User view"""

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.setupUi(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.passwd_confirm.setEchoMode(QLineEdit.Password)
        self._user_create = True

    def set_exist_username(self, **kargs):
        """Username property access"""

        if "username" in kargs.keys():
            self.username.setText(kargs["username"])
        if "password" in kargs.keys():
            self.password.setText(kargs["password"])

    @property
    def user_create(self):
        """Property access"""

        return self._user_create

    @user_create.setter
    def user_create(self, value):
        """Property setter"""

        self._user_create = value
        self.define_view()

    def define_view(self):
        """Define what to show/hide in the dialog box"""

        self.label_password.setHidden(self._user_create)
        self.label.setHidden(self._user_create)
        self.passwd_confirm.setHidden(self._user_create)
        self.password.setHidden(self._user_create)


    def reset(self):
        """Reset entries"""

        self.username.setText("")
        self.familyname.setText("")
        self.nickname.setText("")
        self.password.setText("")
        self.passwd_confirm.setText("")


    @pyqtSlot(str)
    def on_status(self, message):

        super(SignUp, self).on_status(message)
