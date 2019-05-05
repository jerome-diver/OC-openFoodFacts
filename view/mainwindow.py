'''Mainwindow Qt-5 application'''

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QModelIndex
from ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    '''Main Window application''' 

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setupUi(self)
        self.openfoodfacts_mode.setChecked(False)
        self.local_mode.setChecked(False)
        self.substitutes_list.verticalHeader().setVisible(False)
        self.statusBar.showMessage("Effectuez une recherche sur Open Food "
                                   "Facts ou authentifiez vous pour accéder "
                                   "à vôtre base de données")

    def show_categories(self, model):
        '''Show model inside the categories list view'''

        self.categories_list.setModel(model)
        self.statusBar.showMessage("Catégories affichées")
        self.categories_list.show()

    def show_foods(self, model):
        '''Show model inside the foods list view'''

        self.foods_list.setModel(model)
        self.statusBar.showMessage("Liste des produits relatifs à la "
                                   "catégorie sélectionnée affichées")
        self.foods_list.show()

    def show_substitutes(self, model):
        '''Show moedl inside substitutes table view'''

        self.substitutes_list.setModel(model)
        self.statusBar.showMessage("Produits possibles de substitutions "
                                   "proposées avec leur score affichées")
        self.substitutes_list.show()

    @pyqtSlot(QModelIndex)
    def on_category_selected(self):
        model = self.substitutes_list.model()
        if model:
            model.removeRows(0, model.rowCount())

    @pyqtSlot(str)
    def on_status_message(self, message):
        self.statusBar.showMessage(message)