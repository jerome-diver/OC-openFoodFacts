# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 1009)
        MainWindow.setMinimumSize(QtCore.QSize(1050, 800))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/assets/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_user_mode = QtWidgets.QHBoxLayout()
        self.horizontalLayout_user_mode.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_user_mode.setObjectName("horizontalLayout_user_mode")
        self.users_box = QtWidgets.QGroupBox(self.centralwidget)
        self.users_box.setMinimumSize(QtCore.QSize(200, 200))
        self.users_box.setMaximumSize(QtCore.QSize(300, 250))
        self.users_box.setObjectName("users_box")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.users_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.signin = QtWidgets.QPushButton(self.users_box)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        self.signin.setFont(font)
        self.signin.setObjectName("signin")
        self.verticalLayout.addWidget(self.signin)
        self.signup = QtWidgets.QPushButton(self.users_box)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        self.signup.setFont(font)
        self.signup.setObjectName("signup")
        self.verticalLayout.addWidget(self.signup)
        self.frame_2 = QtWidgets.QFrame(self.users_box)
        self.frame_2.setStyleSheet("border-image: url(:/images/assets/images/home 1.png);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout.addWidget(self.frame_2)
        self.horizontalLayout_user_mode.addWidget(self.users_box)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(250, 150))
        self.frame.setStyleSheet("border-image: url(:/images/assets/images/openfoodfacts+oc.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_user_mode.addWidget(self.frame)
        self.substitute_mode_box = QtWidgets.QGroupBox(self.centralwidget)
        self.substitute_mode_box.setMinimumSize(QtCore.QSize(200, 200))
        self.substitute_mode_box.setMaximumSize(QtCore.QSize(300, 250))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setUnderline(True)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.substitute_mode_box.setFont(font)
        self.substitute_mode_box.setObjectName("substitute_mode_box")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.substitute_mode_box)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.openfoodfacts_mode = QtWidgets.QPushButton(self.substitute_mode_box)
        self.openfoodfacts_mode.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openfoodfacts_mode.sizePolicy().hasHeightForWidth())
        self.openfoodfacts_mode.setSizePolicy(sizePolicy)
        self.openfoodfacts_mode.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.openfoodfacts_mode.setFont(font)
        self.openfoodfacts_mode.setIcon(icon)
        self.openfoodfacts_mode.setCheckable(True)
        self.openfoodfacts_mode.setChecked(False)
        self.openfoodfacts_mode.setAutoDefault(False)
        self.openfoodfacts_mode.setDefault(False)
        self.openfoodfacts_mode.setFlat(False)
        self.openfoodfacts_mode.setObjectName("openfoodfacts_mode")
        self.verticalLayout_2.addWidget(self.openfoodfacts_mode)
        self.local_mode = QtWidgets.QPushButton(self.substitute_mode_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.local_mode.sizePolicy().hasHeightForWidth())
        self.local_mode.setSizePolicy(sizePolicy)
        self.local_mode.setMinimumSize(QtCore.QSize(0, 0))
        self.local_mode.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.local_mode.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/assets/images/home 1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.local_mode.setIcon(icon1)
        self.local_mode.setCheckable(True)
        self.local_mode.setObjectName("local_mode")
        self.verticalLayout_2.addWidget(self.local_mode)
        self.quit = QtWidgets.QPushButton(self.substitute_mode_box)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.quit.setFont(font)
        self.quit.setObjectName("quit")
        self.verticalLayout_2.addWidget(self.quit)
        self.horizontalLayout_user_mode.addWidget(self.substitute_mode_box)
        self.verticalLayout_7.addLayout(self.horizontalLayout_user_mode)
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.categories_grp = QtWidgets.QGroupBox(self.splitter_2)
        self.categories_grp.setMinimumSize(QtCore.QSize(0, 300))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setUnderline(True)
        self.categories_grp.setFont(font)
        self.categories_grp.setObjectName("categories_grp")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.categories_grp)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.categories_list = QtWidgets.QListView(self.categories_grp)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setUnderline(False)
        self.categories_list.setFont(font)
        self.categories_list.setObjectName("categories_list")
        self.verticalLayout_4.addWidget(self.categories_list)
        self.foods_grp = QtWidgets.QGroupBox(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setUnderline(True)
        self.foods_grp.setFont(font)
        self.foods_grp.setObjectName("foods_grp")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.foods_grp)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.foods_list = QtWidgets.QListView(self.foods_grp)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setUnderline(False)
        self.foods_list.setFont(font)
        self.foods_list.setObjectName("foods_list")
        self.verticalLayout_3.addWidget(self.foods_list)
        self.verticalLayout_7.addWidget(self.splitter_2)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setUnderline(True)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.splitter = QtWidgets.QSplitter(self.groupBox)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.substitutes_list = QtWidgets.QTableView(self.splitter)
        self.substitutes_list.setMinimumSize(QtCore.QSize(400, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(False)
        self.substitutes_list.setFont(font)
        self.substitutes_list.setObjectName("substitutes_list")
        self.substitute_selected_grp = QtWidgets.QGroupBox(self.splitter)
        self.substitute_selected_grp.setMaximumSize(QtCore.QSize(650, 16777215))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setUnderline(True)
        self.substitute_selected_grp.setFont(font)
        self.substitute_selected_grp.setObjectName("substitute_selected_grp")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.substitute_selected_grp)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.substitute_widget = QtWidgets.QWidget(self.substitute_selected_grp)
        self.substitute_widget.setMaximumSize(QtCore.QSize(650, 16777215))
        self.substitute_widget.setAccessibleName("")
        self.substitute_widget.setObjectName("substitute_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.substitute_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_url = QtWidgets.QLabel(self.substitute_widget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(8)
        font.setUnderline(False)
        self.label_url.setFont(font)
        self.label_url.setObjectName("label_url")
        self.gridLayout.addWidget(self.label_url, 9, 0, 1, 1)
        self.product_url = QLabelClickable(self.substitute_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.product_url.sizePolicy().hasHeightForWidth())
        self.product_url.setSizePolicy(sizePolicy)
        self.product_url.setMaximumSize(QtCore.QSize(600, 16777215))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setUnderline(False)
        self.product_url.setFont(font)
        self.product_url.setObjectName("product_url")
        self.gridLayout.addWidget(self.product_url, 9, 2, 1, 1)
        self.product_brand = QtWidgets.QLineEdit(self.substitute_widget)
        self.product_brand.setMaximumSize(QtCore.QSize(400, 16777215))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setUnderline(False)
        self.product_brand.setFont(font)
        self.product_brand.setObjectName("product_brand")
        self.gridLayout.addWidget(self.product_brand, 1, 2, 1, 1)
        self.product_name = QtWidgets.QLabel(self.substitute_widget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setUnderline(False)
        self.product_name.setFont(font)
        self.product_name.setText("")
        self.product_name.setObjectName("product_name")
        self.gridLayout.addWidget(self.product_name, 0, 2, 1, 2)
        self.label_packaging = QtWidgets.QLabel(self.substitute_widget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(8)
        font.setUnderline(False)
        self.label_packaging.setFont(font)
        self.label_packaging.setObjectName("label_packaging")
        self.gridLayout.addWidget(self.label_packaging, 2, 0, 1, 1)
        self.label_nom = QtWidgets.QLabel(self.substitute_widget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(8)
        font.setUnderline(False)
        self.label_nom.setFont(font)
        self.label_nom.setObjectName("label_nom")
        self.gridLayout.addWidget(self.label_nom, 0, 0, 1, 1)
        self.label_description = QtWidgets.QLabel(self.substitute_widget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(8)
        font.setUnderline(False)
        self.label_description.setFont(font)
        self.label_description.setLineWidth(-1)
        self.label_description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_description.setObjectName("label_description")
        self.gridLayout.addWidget(self.label_description, 8, 0, 1, 1)
        self.label_brand = QtWidgets.QLabel(self.substitute_widget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(8)
        font.setUnderline(False)
        self.label_brand.setFont(font)
        self.label_brand.setObjectName("label_brand")
        self.gridLayout.addWidget(self.label_brand, 1, 0, 1, 1)
        self.product_shops = QtWidgets.QListView(self.substitute_widget)
        self.product_shops.setMaximumSize(QtCore.QSize(400, 16777215))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setUnderline(False)
        self.product_shops.setFont(font)
        self.product_shops.setObjectName("product_shops")
        self.gridLayout.addWidget(self.product_shops, 7, 2, 1, 1)
        self.label_score = QtWidgets.QLabel(self.substitute_widget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(8)
        font.setUnderline(False)
        self.label_score.setFont(font)
        self.label_score.setObjectName("label_score")
        self.gridLayout.addWidget(self.label_score, 4, 0, 1, 1)
        self.label_shops = QtWidgets.QLabel(self.substitute_widget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(8)
        font.setUnderline(False)
        self.label_shops.setFont(font)
        self.label_shops.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_shops.setObjectName("label_shops")
        self.gridLayout.addWidget(self.label_shops, 7, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 4, 1, 1)
        self.product_img_thumb = QtWidgets.QLabel(self.substitute_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.product_img_thumb.sizePolicy().hasHeightForWidth())
        self.product_img_thumb.setSizePolicy(sizePolicy)
        self.product_img_thumb.setMinimumSize(QtCore.QSize(150, 200))
        self.product_img_thumb.setMaximumSize(QtCore.QSize(150, 200))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(False)
        self.product_img_thumb.setFont(font)
        self.product_img_thumb.setAccessibleName("")
        self.product_img_thumb.setAutoFillBackground(False)
        self.product_img_thumb.setStyleSheet("border-image: url(:/images/assets/images/off logo_thumb.png);")
        self.product_img_thumb.setText("")
        self.product_img_thumb.setAlignment(QtCore.Qt.AlignCenter)
        self.product_img_thumb.setObjectName("product_img_thumb")
        self.gridLayout.addWidget(self.product_img_thumb, 1, 3, 7, 1)
        self.label_code = QtWidgets.QLabel(self.substitute_widget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setUnderline(False)
        self.label_code.setFont(font)
        self.label_code.setObjectName("label_code")
        self.gridLayout.addWidget(self.label_code, 3, 0, 1, 1)
        self.product_packaging = QtWidgets.QLineEdit(self.substitute_widget)
        self.product_packaging.setMaximumSize(QtCore.QSize(400, 16777215))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setUnderline(False)
        self.product_packaging.setFont(font)
        self.product_packaging.setObjectName("product_packaging")
        self.gridLayout.addWidget(self.product_packaging, 2, 2, 1, 1)
        self.product_description = QtWidgets.QTextEdit(self.substitute_widget)
        self.product_description.setMaximumSize(QtCore.QSize(650, 16777215))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setUnderline(False)
        self.product_description.setFont(font)
        self.product_description.setAcceptDrops(False)
        self.product_description.setAutoFillBackground(False)
        self.product_description.setReadOnly(True)
        self.product_description.setObjectName("product_description")
        self.gridLayout.addWidget(self.product_description, 8, 2, 1, 2)
        self.product_score = QtWidgets.QLabel(self.substitute_widget)
        self.product_score.setMinimumSize(QtCore.QSize(120, 40))
        self.product_score.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setUnderline(False)
        self.product_score.setFont(font)
        self.product_score.setText("")
        self.product_score.setObjectName("product_score")
        self.gridLayout.addWidget(self.product_score, 4, 2, 1, 1)
        self.product_code = QtWidgets.QLabel(self.substitute_widget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        self.product_code.setFont(font)
        self.product_code.setText("")
        self.product_code.setObjectName("product_code")
        self.gridLayout.addWidget(self.product_code, 3, 2, 1, 1)
        self.verticalLayout_5.addWidget(self.substitute_widget)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.verticalLayout_6.addWidget(self.splitter)
        self.record = QtWidgets.QPushButton(self.groupBox)
        self.record.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.record.setFont(font)
        self.record.setObjectName("record")
        self.verticalLayout_6.addWidget(self.record)
        self.verticalLayout_7.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.statusBar.setFont(font)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OpenFoodFacts Food Substitutions (OpeClassRooms projet-5)"))
        self.users_box.setTitle(_translate("MainWindow", "Utilisateur"))
        self.signin.setText(_translate("MainWindow", "Sign-in"))
        self.signup.setText(_translate("MainWindow", "Sign-up"))
        self.substitute_mode_box.setTitle(_translate("MainWindow", "Reherche de substitution d\'aliment"))
        self.openfoodfacts_mode.setText(_translate("MainWindow", "List OpenFoodFacts"))
        self.local_mode.setText(_translate("MainWindow", "Liste locale"))
        self.quit.setText(_translate("MainWindow", "Quitter"))
        self.categories_grp.setTitle(_translate("MainWindow", "Sélectionnez une catégorie"))
        self.foods_grp.setTitle(_translate("MainWindow", "Sélectionnez un aliment"))
        self.groupBox.setTitle(_translate("MainWindow", "Substituts proposés"))
        self.substitute_selected_grp.setTitle(_translate("MainWindow", "Détails"))
        self.label_url.setText(_translate("MainWindow", "url"))
        self.product_url.setText(_translate("MainWindow", "url..."))
        self.label_packaging.setText(_translate("MainWindow", "Packaging"))
        self.label_nom.setText(_translate("MainWindow", "Nom"))
        self.label_description.setText(_translate("MainWindow", "Description"))
        self.label_brand.setText(_translate("MainWindow", "Marque"))
        self.label_score.setText(_translate("MainWindow", "Score"))
        self.label_shops.setText(_translate("MainWindow", "Magasins"))
        self.label_code.setText(_translate("MainWindow", "Code"))
        self.record.setText(_translate("MainWindow", "Enregistrer dans ma base"))


from assets.objects.qlabel_clickable import QLabelClickable
import ui.images_rc
