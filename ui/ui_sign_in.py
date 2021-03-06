# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sign-in.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SignIn(object):
    """From Qt Designer, make a PyQt5 Graphic User Interface"""

    def setupUi(self, SignIn):
        """ Setup the GUI"""

        SignIn.setObjectName("SignIn")
        SignIn.resize(400, 200)
        SignIn.setMinimumSize(QtCore.QSize(400, 200))
        SignIn.setMaximumSize(QtCore.QSize(600, 200))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/assets/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SignIn.setWindowIcon(icon)
        SignIn.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(SignIn)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_username = QtWidgets.QLabel(SignIn)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(9)
        self.label_username.setFont(font)
        self.label_username.setObjectName("label_username")
        self.gridLayout.addWidget(self.label_username, 0, 0, 1, 1)
        self.label_password = QtWidgets.QLabel(SignIn)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(9)
        self.label_password.setFont(font)
        self.label_password.setObjectName("label_password")
        self.gridLayout.addWidget(self.label_password, 1, 0, 1, 1)
        self.username = QtWidgets.QLineEdit(SignIn)
        self.username.setObjectName("username")
        self.gridLayout.addWidget(self.username, 0, 1, 1, 1)
        self.password = QtWidgets.QLineEdit(SignIn)
        self.password.setInputMethodHints(QtCore.Qt.ImhSensitiveData)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.frame = QtWidgets.QFrame(SignIn)
        self.frame.setStyleSheet("border-image: url(:/images/assets/images/OpenClassRooms__clair__1.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 73, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.status = QtWidgets.QLabel(SignIn)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.status.setFont(font)
        self.status.setText("")
        self.status.setObjectName("status")
        self.horizontalLayout.addWidget(self.status)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.connection = QtWidgets.QPushButton(SignIn)
        self.connection.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.connection.setFont(font)
        self.connection.setObjectName("connection")
        self.horizontalLayout.addWidget(self.connection)
        self.cancel = QtWidgets.QPushButton(SignIn)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.cancel.setFont(font)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SignIn)
        QtCore.QMetaObject.connectSlotsByName(SignIn)

    def retranslateUi(self, SignIn):
        """Give a translatable name of QWidgets Labels texts"""

        _translate = QtCore.QCoreApplication.translate
        SignIn.setWindowTitle(_translate("SignIn", "Connexion à la base de donnée locale"))
        self.label_username.setText(_translate("SignIn", "nom d\'utilisateur"))
        self.label_password.setText(_translate("SignIn", "mot de passe"))
        self.connection.setText(_translate("SignIn", "Connecter"))
        self.cancel.setText(_translate("SignIn", "Annuler"))


import ui.images_rc
