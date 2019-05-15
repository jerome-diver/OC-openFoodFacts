'''Mainwindow Qt-5 application'''

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    '''Main Window application''' 

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setupUi(self)
        self.record.setDisabled(True)
        self.openfoodfacts_mode.setChecked(False)
        self.local_mode.setChecked(False)
        self.substitutes_list.verticalHeader().setVisible(False)
        self.product_name.setOpenExternalLinks(True)
        self.statusBar.showMessage("Effectuez une recherche sur Open Food "
                                   "Facts ou authentifiez vous pour accéder "
                                   "à vôtre base de données")

    def show_categories(self, model):
        '''Show model inside the categories list view'''

        self.categories_list.setModel(model)
        self.statusBar.showMessage("Catégories affichées")
        self.categories_list.show()

    def show_substitutes(self, model):
        '''Show model inside substitutes table view'''

        self.substitutes_list.setModel(model)
        self.statusBar.showMessage("Produits possibles de substitutions "
                                   "proposées avec leur score affichées")
        self.substitutes_list.setColumnHidden(2, True)
        header = self.substitutes_list.horizontalHeader()
        header.setStretchLastSection(True)
        self.substitutes_list.resizeColumnsToContents()
        self.substitutes_list.show()

    def show_product_details(self, model):
        '''Sow models for all details of product selected'''

        self.statusBar.showMessage("Détails du produit sélectionné "
                                   "affichés")
        self.product_name.setText(model["name"])
        self.product_brand.setText(model["brand"])
        self.product_packaging.setText(model["packaging"])
        self.product_code.setText(model["code"])
        if isinstance(model["score"], QPixmap):
            self.product_score.setPixmap(model["score"])
            self.product_score.setScaledContents(True)
        else:
            self.product_score.setText(model["score"])
        self.product_shops.setModel(model["shops"])
        self.product_description.setText(model["description"])
        self.product_url.setText(model["url"])
        if isinstance(model["score"], QPixmap):
            self.product_img_thumb.setPixmap(model["img_thumb"])
            self.product_img_thumb.setScaledContents(True)

    def reset_views(self, views=["all"]):
        empty_model = QStandardItemModel()
        if "categories" in views or "all" in views:
            self.categories_list.setModel(empty_model)
        if "foods" in views or "all" in views:
            self.foods_list.setModel(empty_model)
        if "substitutes" in views or "all" in views:
            self.substitutes_list.setModel(empty_model)
        if "details" in views or "all" in views:
            self.product_name.setText("")
            self.product_brand.setText("")
            self.product_packaging.setText("")
            self.product_shops.setModel(empty_model)
            self.product_score.setText("")
            self.product_description.setText("")
            self.product_url.setText("")
            self.product_img_thumb.setText("")
            self.product_score.setPixmap(QPixmap())
            self.product_img_thumb.setPixmap(QPixmap())

    @pyqtSlot(str)
    def on_status_message(self, message):
        self.statusBar.showMessage(message)

    @pyqtSlot(str)
    def on_error_message(self, message):
        QMessageBox.information(self, "Erreur de données", message)