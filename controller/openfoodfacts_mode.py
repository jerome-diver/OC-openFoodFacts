'''Controller for OpenFoodFacts API access mode'''

from model import OpenFoodFacts
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QModelIndex, QThread


class OpenFoodFactsMode(QObject):
    '''Print OpenFoodFacts substitutions food 
    selected for category list and food list'''

    status_message = pyqtSignal(str)

    def __init__(self, window, database):
        super().__init__()
        self._window = window
        self._database = database
        self._views = { "categories": self._window.categories_list,
                        "foods": self._window.foods_list,
                        "substitutes": self._window.substitutes_list,
                        "name" : self._window.substitute_name,
                        "description" : self._window.substitute_description,
                        "shops" : self._window.substitute_shops,
                        "url" : self._window.substitute_url,
                        "score" : self._window.substitute_score
                       }
        self._model = OpenFoodFacts(self._database, self._views)
        self._load_categories = LoadCategories(self._model)
        self._load_foods = LoadFoods(self._model)
        self._load_product_details = LoadProductDetails(self._model)
        self.connect_signals()
        self._load_categories.start()
        self.status_message.emit("Patientez, recherche des catégories "
                                 "disponibles en cours sur Open Food "
                                 "Facts...")


    def connect_signals(self):
        '''Let's connect signals to slots for concerned controller'''

        self._window.categories_list.clicked.connect(
            self._model.reset_substitute_list)
        self._window.categories_list.clicked.connect(
            self.on_category_selected)
        self._window.foods_list.clicked.connect(
            self._model.reset_product_details)
        self._window.foods_list.clicked.connect(
            self.on_food_selected)
        self._window.substitutes_list.clicked.connect(
            self.on_product_selected)
        self.status_message.connect(
            self._window.on_status_message)
        self._load_categories.finished.connect(
            self.on_load_categories_finished)
        self._load_foods.finished.connect(
            self.on_load_foods_finished)
        self._load_product_details.finished.connect(
            self.on_load_product_details_finished)

    @pyqtSlot()
    def on_load_categories_finished(self):
        '''Show categories of products food
        from openFoodFacts model in view'''

        self._window.show_categories(self._model.categories)

    @pyqtSlot()
    def on_load_foods_finished(self):
        '''Show food's products from Open Food Facts'''

        self._window.show_foods(self._model.foods)

    @pyqtSlot()
    def on_load_product_details_finished(self):
        '''Show details of product from Open Food Facts'''

        self._window.show_product_details(self._model.details)

    @pyqtSlot(QModelIndex)
    def on_category_selected(self, index):
        '''Slot for next action on clicked category selection from
        category list view'''

        self.status_message.emit("Patientez, recherche des produits "
                                 "relatifs à la catégorie en cours "
                                 "sur Open Food Facts...")
        self._load_foods.category = index.data()
        self._load_foods.start()

    @pyqtSlot(QModelIndex)
    def on_food_selected(self, index):
        '''Slot for next action on clicked foods selection from
        foods list view'''

        self.status_message.emit("Patientez, recherche des produits "
                                 "de substitutions proposés en cours "
                                 "sur Open Food Facts...")
        food_selected = index.data
        self._model.populate_substitutes(food_selected)
        self._window.show_substitutes(self._model.substitutes)

    @pyqtSlot(QModelIndex)
    def on_product_selected(self, index):
        '''Slot for next action after selected a substitute's product'''

        code = self._views["substitutes"].model().index(index.row(), 2).data()
        self.status_message.emit("Patientez, recherche sur le code produit "
                                 "{}".format(code))
        self._load_product_details.code = code
        self._load_product_details.start()

class LoadCategories(QThread):
    '''Load Categories model in background process to not freeze
    thz application'''

    def __init__(self, model):
        super().__init__()
        self._model = model

    def __del__(self):
        self.wait()

    def run(self):
        '''Start running the thread for populate model of Open Food Facts
        categories list'''

        self._model.populate_categories()

class LoadFoods(QThread):
    '''Load foods model in background to not freeze application'''

    def __init__(self, model):
        super().__init__()
        self._model = model
        self._category = ''

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    def __del__(self):
        self.wait()

    def run(self):
        '''Start running thread to load model for foods list from
        Open Food Facts'''

        self._model.populate_foods(self._category)

class LoadProductDetails(QThread):
    '''Load product selected from substitutes list to create model
    for details'''

    def __init__(self, model):
        super().__init__()
        self._model = model
        self._code = ""

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    def __del__(self):
        self.wait()

    def run(self):
        '''Start to load details of product in background from Open Food
        Facts'''

        self._model.populate_product_details(self._code)
