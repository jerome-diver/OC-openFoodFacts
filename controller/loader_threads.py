'''Module For threads loaders to run Open Food Facts request call on
background to not freeze application'''

from math import ceil
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread

from model import OpenFoodFacts
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
            categories.append(row)
        if not categories:
            categories = self._model.download_categories()
        self._model.categories.populate(categories)


class LoadFoods(QThread):
    '''Load foods model in background to not freeze application'''

    get_a_page = pyqtSignal(int, int)
    no_product_found = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self._model = model
        self._category = ''

    @property
    def category(self):
        '''Return property of category name'''

        return self._category

    @category.setter
    def category(self, value):
        '''Setter for property of category name'''

        self._category = value

    def __del__(self):
        self.wait()

    def run(self):
        '''Start running thread to load model for foods list from
        Open Food Facts'''

        page = 1
        pages_to_end = 1
        while pages_to_end != 0:
            first_page = bool(page == 1)
            foods = self._model.download_foods(self._category, page)
            if foods:
                self._model.foods.recorded.append(foods)
                if first_page:
                    products = self._model.foods.count
                    pages_to_end = ceil(products / 20) - 1
                self._model.foods.populate(foods, first_page)
                self.get_a_page.emit(page, pages_to_end)
            else:
                self.no_product_found.emit()
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
        '''Return property for product name substitute'''

        return self._name

    @name.setter
    def name(self, value):
        '''Setter property for name of substitute product'''

        self._name = value

    @property
    def code(self):
        '''Return property for code product substitute'''

        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    def __del__(self):
        self.wait()

    def run(self):
        '''Start to load details of product in background from Open Food
        Facts'''

        mpd = self._model.product_details
        ms = self._model.substitutes
        mpd.reset()
        self.status_message.emit("Patientez, recherche du produit "
                                 "(code {} ) en cours sur "
                                 "Open Food Facts...".format(self._code))
        food = self._model.download_product(self._code, self._name)
        if food:
            mpd.populate(food)
            if DEBUG_MODE:
                print("search in list for:", food["codes_tags"][1])
            if food["codes_tags"][1] in ms.checked:
                mpd.checked[food["codes_tags"][1]] = (
                    mpd.models["name"],
                    mpd.models["description"],
                    mpd.models["score_data"],
                    mpd.models["brand"],
                    mpd.models["packaging"],
                    mpd.models["url"],
                    mpd.models["img_data"])
            else:
                if food["codes_tags"][1] in mpd.checked.keys():
                    del mpd.checked[food["codes_tags"][1]]
            if DEBUG_MODE:
                print("list checked:", mpd.checked)
        else:
            mpd.reset()
            self.error_signal.emit("Hélas, il n'y a aucun détail enregistré "
                                   "pour ce code produit")
            self.status_message.emit("Aucun détail cohérent n'est fourni")


class UpdateCategories(QThread):
    '''Load categories from Open Food Facts in background in categroies
    table of the openfoodfacts_substitutes database'''

    def __init__(self, database, off_model):
        super().__init__()
        self._database = database
        self._off_model = off_model

    def __del__(self):
        self.wait()

    def run(self):
        '''Start thread job'''

        if DEBUG_MODE:
            print("start to update categories table from OFF categories")
        categories = self._off_model.download_categories()
        if categories:
            self._database.update_categories(categories)
        if DEBUG_MODE:
            print("End of update categories table")
