"""Mainwindow Qt-5 application"""

import re
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QPixmap
from PyQt5.QtCore import pyqtSlot, QSortFilterProxyModel

from ui import Ui_MainWindow
from controller import Widget


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window application"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setupUi(self)
        self.record.setDisabled(True)
        self.openfoodfacts_mode.setChecked(False)
        self.local_mode.setChecked(False)
        self.substitutes_list.verticalHeader().setVisible(False)
        self.product_name.setOpenExternalLinks(True)
        self._proxy = QSortFilterProxyModel()
        self.substitutes_list.setModel(self._proxy)

    def show_categories(self, model):
        """Show model inside the categories list view"""

        self.categories_list.setModel(model)
        self.statusBar.showMessage("Catégories affichées")
        self.categories_list.show()

    def show_foods(self, model):
        """Show model inside the foods table view"""

        self.foods_list.setModel(model)
        self.statusBar.showMessage("Produits affichés")
        self.foods_list.show()

    def show_substitutes(self, model):
        """Show model inside substitutes table view"""

        self._proxy.setSourceModel(model)
        self.substitutes_list.setModel(self._proxy)
        self.substitutes_list.setColumnHidden(2, True)
        header = self.substitutes_list.horizontalHeader()
        header.setStretchLastSection(True)
        self.substitutes_list.resizeColumnsToContents()
        self.substitutes_list.show()

    def show_product_details(self, models):
        """Sow modelss for all details of product selected"""

        self.statusBar.showMessage("Détails du produit sélectionné "
                                   "trouvés et affichés")
        self.product_name.setText(models["name"])
        self.product_brand.setText(models["brand"])
        self.product_packaging.setText(models["packaging"])
        self.product_code.setText(models["code"])
        if isinstance(models["score"], QPixmap):
            self.product_score.setPixmap(models["score"])
            self.product_score.setScaledContents(True)
        else:
            self.product_score.setText(models["score"])
        self.product_shops.setModel(models["shops"])
        self.product_description.setText(models["description"])
        self.product_url.setText(models["url"])
        if isinstance(models["score"], QPixmap):
            self.product_img_thumb.setPixmap(models["img_thumb"])
            self.product_img_thumb.setScaledContents(True)

    def reset_views(self, views=(Widget.ALL,)):
        """Reset all views of MainWindow"""

        empty_model = QStandardItemModel()
        if Widget.CATEGORIES in views or Widget.ALL in views:
            self.categories_list.setModel(empty_model)
        if Widget.FOODS in views or Widget.ALL in views:
            self.foods_list.setModel(empty_model)
        if Widget.SUBSTITUTES in views or Widget.ALL in views:
            self._proxy.setSourceModel(empty_model)
            self.substitutes_list.setModel(self._proxy)
        if Widget.DETAILS in views or Widget.ALL in views:
            self.product_name.setText("")
            self.product_code.setText("")
            self.product_brand.setText("")
            self.product_packaging.setText("")
            self.product_shops.setModel(empty_model)
            self.product_score.setText("")
            self.product_description.setText("")
            self.product_url.setText("")
            self.product_img_thumb.setText("")
            self.product_img_thumb.setPixmap(QPixmap())
            self.product_score.setPixmap(QPixmap())
            self.product_img_thumb.setPixmap(QPixmap())

    def get_bg_color(self):
        """Return stylesheet background color tuple of int"""

        bg_isolate = re.sub(r'^background-color: rgb\((\d+)\,\s(\d+)\,'
                            r'\s(\d+)\);',
                            r'\1,\2,\3', self.styleSheet())
        return tuple(int(x) for x in re.split(r'\,', bg_isolate))

    @pyqtSlot(str)
    def on_status_message(self, message):
        """Slot for status message signal emited from anywhere"""

        self.statusBar.showMessage(message)

    @pyqtSlot(str)
    def on_error_message(self, message):
        """Slot for error message signal send from anywhere"""

        QMessageBox.information(self, "Erreur de données", message)
