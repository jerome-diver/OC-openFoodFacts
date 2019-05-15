'''Module For threads loaders to run Open Food Facts request call on
background to not freeze application'''

from PyQt5.QtCore import pyqtSignal, QThread
from model import OpenFoodFacts
from math import ceil
from settings import DEBUG_MODE

class LoadCategories(QThread):
    '''Load Categories model in background process to not freeze
    thz application'''

    def __init__(self, model, database):
        super().__init__()
        self._model = model
        self._database = database

    def __del__(self):
        self.wait()

    def run(self):
        '''Start running the thread for populate model of Open Food Facts
        categories list from local database or from Open Food Facts API
        online'''

        categories = []
        request = "SELECT id, name FROM categories ORDER BY name;"
        for row in  self._database.ask_request(request):
            categories.append( row )
        if not categories:
            categories = self._model.download_categories()
        self._model.populate_categories(categories)


class LoadFoods(QThread):
    '''Load foods model in background to not freeze application'''

    get_a_page = pyqtSignal(int, int)

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
        self._model._selected_category = value

    def __del__(self):
        self.wait()

    def run(self):
        '''Start running thread to load model for foods list from
        Open Food Facts'''

        page = 1
        pages_to_end = 1
        while pages_to_end != 0:
            state = True if page == 1 else False
            foods = self._model.download_foods(self._category, page)
            self._model._foods_recorded.append(foods)
            if page == 1:
                products = self._model.products_count
                pages_to_end = ceil(products / 20) - 1
            self._model.populate_foods(foods, state)
            self.get_a_page.emit(page, pages_to_end)
            page += 1
            pages_to_end -= 1


class LoadProductDetails(QThread):
    '''Load product selected from substitutes list to create model
    for details'''

    error_signal = pyqtSignal(str)
    status_message = pyqtSignal(str)

    def __init__(self, model):
        super().__init__()
        self._model = model
        self._code = ""
        self._name = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

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

        self._model.reset_product_details()
        self.status_message.emit("Patientez, recherche du produit "
                                 "(code {} ) en cours sur "
                                 "Open Food Facts...".format(self._code))
        food = self._model.download_product(self._code, self._name)
        if food:
            self._model.populate_product_details(food)
            # record details if caller is checked...
            if DEBUG_MODE:
                print("search in list for:", food["codes_tags"][1])
            if food["codes_tags"][1] in self._model.checked_substitutes_list:
                self._model.checked_details_dict[food["codes_tags"][1]] = (
                              self._model.details["name"],
                              self._model.details["description"],
                              self._model.details["score_data"],
                              self._model.details["brand"],
                              self._model.details["packaging"],
                              self._model.details["url"],
                              self._model.details["img_data"] )
            else:
                if food["codes_tags"][1] in self._model.checked_details_dict.keys():
                    del self._model.checked_details_dict[food["codes_tags"][1]]
            if DEBUG_MODE:
                print("list checked:", self._model.checked_details_dict)
        else:
            self._model.reset_product_details()
            self.error_signal.emit("Hélas, il n'y a aucun détail enregistré "
                                   "pour ce code produit")
            self.status_message.emit("Aucun détail cohérent n'est fourni")


class UpdateCategories(QThread):
    '''Load categories from Open Food Facts in background in categroies
    table of the openfoodfacts_substitutes database'''

    def __init__(self, database):
        super().__init__()
        self._database = database

    def __del__(self):
        self.wait()

    def run(self):
        '''Start thread job'''

        if DEBUG_MODE:
            print("start to update categories table from OFF categories")
        off_model = OpenFoodFacts()
        categories = off_model.download_categories()
        self._database.update_categories(categories)
        if DEBUG_MODE:
            print("End of update categories table")
