'''Module For threads loaders to run Open Food Facts request call on
background to not freeze application'''

from PyQt5.QtCore import pyqtSignal, QThread
from model import OpenFoodFacts
from math import ceil
from settings import REQUEST_PAGE_SIZE


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
        request = "SELECT item_id AS 'id', item_name AS 'name' " \
                  "FROM categories ;"
        for row in  self._database.ask_request(request):
            categories.append( row )
        if not categories:
            categories = self._model.download_categories()
        self._model.populate_categories(categories)


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

        self._model.reset_product_details()
        self._model.populate_product_details(self._code)


class CheckProductCodeExist(QThread):
    '''Check that the product with this code exist in the openfoodfacts
    database'''

    empty_product = pyqtSignal(str)

    def __init__(self, model):
        super().__init__()
        self._model = model
        self._codes = []

    def __del__(self):
        self.wait()

    @property
    def codes(self):
        return self._codes

    @codes.setter
    def codes(self, _list):
        self._codes = _list

    def run(self):
        '''Run searching with openfoodfacts api if product exist'''

        for code in self._codes:
            product = self._model.get_product(code)
            if not product:
                self.empty_product.emit(code)

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

        print("start to update categories table from OFF categories")
        off_model = OpenFoodFacts()
        categories = off_model.download_categories()
        self._database.update_categories(categories)
