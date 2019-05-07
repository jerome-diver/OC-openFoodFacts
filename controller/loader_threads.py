'''Module For threads loaders to run Open Food Facts request call on
background to not freeze application'''

from PyQt5.QtCore import pyqtSignal, QThread


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
