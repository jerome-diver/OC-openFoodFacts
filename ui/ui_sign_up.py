# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sign-up.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SignUp(object):
    def setupUi(self, SignUp):
        SignUp.setObjectName("SignUp")
        SignUp.resize(600, 300)
        SignUp.setMinimumSize(QtCore.QSize(450, 150))
        SignUp.setMaximumSize(QtCore.QSize(600, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/assets/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SignUp.setWindowIcon(icon)
        SignUp.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(SignUp)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_username = QtWidgets.QLabel(SignUp)
        self.label_username.setObjectName("label_username")
        self.gridLayout.addWidget(self.label_username, 2, 0, 1, 1)
        self.label_password = QtWidgets.QLabel(SignUp)
        self.label_password.setObjectName("label_password")
        self.gridLayout.addWidget(self.label_password, 3, 0, 1, 1)
        self.label_nickname = QtWidgets.QLabel(SignUp)
        self.label_nickname.setObjectName("label_nickname")
        self.gridLayout.addWidget(self.label_nickname, 0, 0, 1, 1)
        self.label_familyname = QtWidgets.QLabel(SignUp)
        self.label_familyname.setObjectName("label_familyname")
        self.gridLayout.addWidget(self.label_familyname, 1, 0, 1, 1)
        self.nickname = QtWidgets.QLineEdit(SignUp)
        self.nickname.setObjectName("nickname")
        self.gridLayout.addWidget(self.nickname, 0, 1, 1, 1)
        self.familyname = QtWidgets.QLineEdit(SignUp)
        self.familyname.setObjectName("familyname")
        self.gridLayout.addWidget(self.familyname, 1, 1, 1, 1)
        self.username = QtWidgets.QLineEdit(SignUp)
        self.username.setObjectName("username")
        self.gridLayout.addWidget(self.username, 2, 1, 1, 1)
        self.password = QtWidgets.QLineEdit(SignUp)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.frame = QtWidgets.QFrame(SignUp)
        self.frame.setStyleSheet("border-image: url(:/images/assets/images/sign_in_localDB_openfoodfacts.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 135, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.status = QtWidgets.QLabel(self.frame)
        self.status.setText("")
        self.status.setObjectName("status")
        self.verticalLayout_2.addWidget(self.status)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.record = QtWidgets.QPushButton(SignUp)
        self.record.setObjectName("record")
        self.horizontalLayout.addWidget(self.record)
        self.cancel = QtWidgets.QPushButton(SignUp)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SignUp)
        QtCore.QMetaObject.connectSlotsByName(SignUp)

    def retranslateUi(self, SignUp):
        _translate = QtCore.QCoreApplication.translate
        SignUp.setWindowTitle(_translate("SignUp", "S\'enregistrer sur la base de donnée locale"))
        self.label_username.setText(_translate("SignUp", "Nom d\'utilisateur"))
        self.label_password.setText(_translate("SignUp", "Mot de passe"))
        self.label_nickname.setText(_translate("SignUp", "Prénom"))
        self.label_familyname.setText(_translate("SignUp", "Nom de famille"))
        self.record.setText(_translate("SignUp", "S\'enregistrer"))
        self.cancel.setText(_translate("SignUp", "Annuler"))


import ui.images_rc
