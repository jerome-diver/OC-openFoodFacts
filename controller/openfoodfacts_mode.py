'''Controller for OpenFoodFacts API access mode'''

import webbrowser
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, \
                         QModelIndex, QItemSelection
from model import OpenFoodFacts
from controller import ThreadsControler, Mode
from settings import DEBUG_MODE


class OpenFoodFactsMode(QObject):
    '''Print OpenFoodFacts substitutions food
    selected for category list and food list'''

    status_message = pyqtSignal(str)
    checked_start = pyqtSignal()
    load_details_finished = pyqtSignal()
    kill_foods_thread = pyqtSignal()

    def __init__(self, window, database):
        super().__init__()
        self._window = window
        self._database = database
        self._internet_flag = False
        self._views = {"categories": self._window.categories_list,
                       "foods": self._window.foods_list,
                       "substitutes": self._window.substitutes_list,
                       "name" : self._window.product_name,
                       "brand" : self._window.product_brand,
                       "packaging" : self._window.product_packaging,
                       "score" : self._window.product_score,
                       "shops" : self._window.product_shops,
                       "description" : self._window.product_description,
                       "url" : self._window.product_url,
                       "img_thumb" : self._window.product_img_thumb,
                       "bg_color": self._window.get_bg_color()}
        self._model = OpenFoodFacts(self._views)
        self._threads = ThreadsControler(self)
        self._no_product = False
        self._flag_mode = Mode.SELECTED
        self.connect_signals()


    def connect_signals(self):
        '''Connect signals to slots for concerned controller'''

        self._views["categories"].clicked.connect(self.on_category_selected)
        self._views["foods"].clicked.connect(self.on_food_selected)
        self._views["substitutes"].selectionModel().selectionChanged.connect(
            self.on_substitute_selection_changed)
        self._model.substitutes.itemChanged.connect(self.on_substitute_checked)
        self._views["url"].clicked.connect(self.on_product_url_clicked)
        self._threads.load_categories.finished.connect(
            self.on_load_categories_finished)
        self._model.internet_access.connect(self.on_internet_access)
        self.status_message.connect(self._window.on_status_message)

    @pyqtSlot()
    def on_load_categories_finished(self):
        '''Show categories of products food
        from openFoodFacts model in view'''

        self._window.show_categories(self._model.categories)

    @pyqtSlot()
    def on_load_foods_finished(self):
        '''Show food's products from Open Food Facts'''

        if not self._no_product:
            self.status_message.emit("Tous les produits de la catégorie sont "
                                     "affichés")
        if DEBUG_MODE:
            print("End process to load foods")

    @pyqtSlot()
    def on_load_product_details_finished(self):
        '''Show details of product from Open Food Facts'''

        if self._flag_mode == Mode.SELECTED:
            self._window.show_product_details(self._model.product_details.models)
        elif self._flag_mode == Mode.CHECKED:
            self.load_details_finished.emit()
            self.status_message.emit("Détails des substituts sélectionnés "
                                     "trouvés")

    @pyqtSlot(int, int)
    def on_new_food_page(self, page, total):
        '''Reload the view for new page added'''

        self.status_message.emit("Affichage des produits en cours... "
                                 "pages: {} affichées | {} restantes".
                                 format(page, total))
        if page == 1:
            self._window.foods_list.setModel(self._model.foods)
        if DEBUG_MODE:
            print("selected food already for:", self._model.foods.selected)
        if self._model.foods.selected:
            self._model.substitutes.populate(self._model.foods.selected,
                                             self._model.foods.recorded,
                                             page - 1, False)

    @pyqtSlot()
    def on_no_product_found(self):
        '''When no product found for category selected happening...'''

        if self._internet_flag:
            self.status_message.emit("Il n'y a aucun produit pour cette catégorie")
        self._model.substitutes.reset()
        self._model.foods.reset()
        self._model.product_details.reset()
        self._window.reset_views(["foods", "substitutes", "details" ])
        self._no_product = True

    @pyqtSlot(bool)
    def on_internet_access(self, status):
        '''When no internet access is happening...'''

        self._internet_flag = status
        self._window.openfoodfacts_mode.setEnabled(status)
        if not status:
            self.status_message.emit("Il n'y a pas d'accès à internet")
            if DEBUG_MODE:
                print("there is no internet access")

    @pyqtSlot(QModelIndex)
    def on_category_selected(self, index):
        '''Slot for next action on clicked category selection from
        category list view'''

        self._no_product = False
        index_id = self._model.categories.index(index.row(), 1)
        self._model.categories.selected = index_id.data()
        if self._model.substitutes:
            self._model.substitutes.reset()
            self._model.product_details.reset()
        self.kill_foods_thread.emit()
        self._threads.init_foods_thread(index.data())
        self.status_message.emit("Patientez, recherche des produits "
                                 "relatifs à la catégorie en cours "
                                 "sur Open Food Facts...")

    @pyqtSlot(QModelIndex)
    def on_food_selected(self, index):
        '''Slot for next action on clicked foods selection from
        foods list view'''

        self._model.substitutes.reset()
        self._model.product_details.reset()
        self.status_message.emit("Patientez, recherche des produits "
                                 "de substitutions proposés en cours "
                                 "sur Open Food Facts...")
        name = index.data()
        code = self._model.foods.index(index.row(), 1).data()
        score = self._model.foods.index(index.row(), 2).data()
        self._model.foods.selected = (code, score, name)
        if DEBUG_MODE:
            print("you are just selecting food:", self._model.foods.selected)
        self._model.substitutes.populate(self._model.foods.selected,
                                         self._model.foods.recorded)
        self.show_substitutes()

    def show_substitutes(self):
        '''Just show substitute products list'''

        self._window.show_substitutes(self._model.substitutes)

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_substitute_selection_changed(self, selected, deselected):
        '''Load details from new selection of substitutes table view'''

        if selected.indexes():
            index_select = selected.indexes()[0]
            self._flag_mode = Mode.SELECTED
            sub_model = self._views["substitutes"].model()
            code = sub_model.index(index_select.row(), 2).data()
            name = sub_model.index(index_select.row(), 0).data()
            if DEBUG_MODE:
                print("now searching product for code", code, "name", name)
            self.status_message.emit("Patientez, recherche sur le code produit "
                                     "{} sélectionné".format(code))
            self._threads.init_product_details_thread(code, name, Mode.SELECTED)

    @pyqtSlot('QStandardItem*')
    def on_substitute_checked(self, item):
        '''Load, from checkbox (substitutes table view) selected, products
        details'''

        self._flag_mode = Mode.CHECKED
        index = self._model.substitutes.indexFromItem(item)
        code = self._model.substitutes.index(index.row(), 2).data()
        name = self._model.substitutes.index(index.row(), 0).data()
        if DEBUG_MODE:
            print("now searching product for code", code, "name", name)
        self.status_message.emit("Patientez, recherche sur le code produit "
                                 "{} à ajouter dans la base".format(code))
        self._threads.init_product_details_thread(code, name, Mode.CHECKED)
        self.checked_start.emit()

    @pyqtSlot()
    def on_product_url_clicked(self):
        '''Go to url'''

        url = self._model.product_details.models["url"]
        webbrowser.open(url)

    @property
    def model(self):
        '''Return model property for OpenFoodFacts instance model'''

        return self._model

    @property
    def database(self):
        '''Database property access'''

        return self._database

    @property
    def window(self):
        '''Window access property'''

        return self._window