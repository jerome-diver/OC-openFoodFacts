'''Controller for OpenFoodFacts API access mode'''

import webbrowser
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, \
                         QModelIndex

from model import OpenFoodFacts
from controller import LoadCategories, LoadFoods, \
                       LoadProductDetails
from settings import DEBUG_MODE


class OpenFoodFactsMode(QObject):
    '''Print OpenFoodFacts substitutions food
    selected for category list and food list'''

    status_message = pyqtSignal(str)
    checked_substitutes_event = pyqtSignal(bool)

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
        self._load_categories = LoadCategories(self._model, self._database)
        self._load_product_details = LoadProductDetails(self._model)
        self._load_foods = None
        self._no_product = False
        self.connect_signals()
        self._load_categories.start()


    def connect_signals(self):
        '''Connect signals to slots for concerned controller'''

        self._window.categories_list.clicked.connect(self.on_category_selected)
        self._window.foods_list.clicked.connect(self.on_food_selected)
        self._window.substitutes_list.clicked.connect(
            self.on_product_selected)
        self._model.substitutes.itemChanged.connect(self.on_substitute_checked)
        self._window.product_url.clicked.connect(self.on_product_url_clicked)
        self._load_categories.finished.connect(
            self.on_load_categories_finished)
        self._load_product_details.finished.connect(
            self.on_load_product_details_finished)
        self._load_product_details.status_message.connect(
            self._window.on_status_message)
        self._load_product_details.error_signal.connect(
            self._window.on_error_message)
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

        self._window.show_product_details(self._model.product_details.models)

    @pyqtSlot(QModelIndex)
    def on_category_selected(self, index):
        '''Slot for next action on clicked category selection from
        category list view'''

        self._no_product = False
        self._model.categories.selected = index.data()
        if self._load_foods:
            if self._load_foods.isRunning():
                self._load_foods.terminate()
                self._load_foods.wait()
        if self._model.foods:
            self._model.foods.reset()
        if self._model.substitutes:
            self._model.substitutes.reset()
            self._model.product_details.reset()
        self._load_foods = LoadFoods(self._model)
        self._load_foods.finished.connect(self.on_load_foods_finished)
        self._load_foods.no_product_found.connect(self.on_no_product_found)
        self._load_foods.get_a_page.connect(self.on_new_food_page)
        self.status_message.emit("Patientez, recherche des produits "
                                 "relatifs à la catégorie en cours "
                                 "sur Open Food Facts...")
        self._load_foods.category = index.data()
        self._load_foods.start()

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
        self._no_product = True

    @pyqtSlot(bool)
    def on_internet_access(self, status):
        '''When no internet access is happening...'''

        self._internet_flag = status
        if not status:
            self.status_message.emit("Il n'y a pas d'accès à internet")
            if DEBUG_MODE:
                print("there is no internet access")

    @pyqtSlot(QModelIndex)
    def on_food_selected(self, index):
        '''Slot for next action on clicked foods selection from
        foods list view'''

        self.status_message.emit("Patientez, recherche des produits "
                                 "de substitutions proposés en cours "
                                 "sur Open Food Facts...")
        food_name = index.data()
        food_code = self._model.foods.index(index.row(), 1).data()
        food_score = self._model.foods.index(index.row(), 2).data()
        self._model.foods.selected = (food_code, food_score, food_name)
        if DEBUG_MODE:
            print("you are just selecting food:", self._model.foods.selected)
        self._model.substitutes.populate(self._model.foods.selected,
                                         self._model.foods.recorded)
        self.show_substitutes()

    def show_substitutes(self):
        '''Just show substitute products list'''

        self._window.show_substitutes(self._model.substitutes)

    @pyqtSlot(QModelIndex)
    def on_product_selected(self, index):
        '''Slot for next action after selected a substitute's product'''

        sub_model = self._views["substitutes"].model()
        index_code = sub_model.index(index.row(), 2)
        index_name = sub_model.index(index.row(), 0)
        code = index_code.data()
        name = index_name.data()
        self.status_message.emit("Patientez, recherche sur le code produit "
                                 "{}".format(code))
        self._load_product_details.code = code
        self._load_product_details.name = name
        self._load_product_details.start()

    @pyqtSlot()
    def on_product_url_clicked(self):
        '''Go to url'''

        url = self._model.product_details.models["url"]
        webbrowser.open(url)

    @pyqtSlot('QStandardItem*')
    def on_substitute_checked(self, item):
        '''From item checkbox selected, add selection to the selected
        substitutes own list'''

        index = self._model.substitutes.indexFromItem(item)
        code = self._model.substitutes.index(index.row(), 2).data()
        self._model.substitutes.generate_checked()
        state = item.checkState()
        if DEBUG_MODE:
            print("i checked this substitute index row:", index.row(),
                  "at column:", index.column(), "code is", code,
                  "and item is checked:", state)
        if state == 2:
            self._model.substitutes.selected.append(code)
        else:
            if code in self._model.substitutes.selected:
                self._model.substitutes.selected.remove(code)
        self.checked_substitutes_event.emit(
            bool(self._model.substitutes.selected))

    @property
    def load_product_details(self):
        '''Return property for QThread instance of LoadProductDetails'''

        return self._load_product_details

    @property
    def model(self):
        '''Return model property for OpenFoodFacts instance model'''

        return self._model