'''Module For threads loaders to run Open Food Facts request call on
background to not freeze application'''

from PyQt5.QtCore import pyqtSignal, QThread
from math import ceil
from settings import REQUEST_PAGE_SIZE


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

        #cat_count = self._model.count_categories()
        #pages = ceil(cat_count / REQUEST_PAGE_SIZE)
        #for n in range(1, pages):
        #    categories = self._model.get_categories_for(n, REQUEST_PAGE_SIZE)
        #    self._model.populate_categories_for(categories)
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
