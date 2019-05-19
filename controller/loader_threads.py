'''Module For threads loaders to run Open Food Facts request call on
background to not freeze application'''

from math import ceil
from enum import Enum
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, \
                         QThread

from settings import DEBUG_MODE


class Mode(Enum):
    '''Enum mode list type'''

    CHECKED = 1
    SELECTED = 2


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
        self._on_air = True

    def __del__(self):
        self.wait()

    @property
    def category(self):
        '''Return property of category name'''

        return self._category

    @category.setter
    def category(self, value):
        '''Setter for property of category name'''

        self._category = value

    @pyqtSlot()
    def end_process(self):
        '''End of the loop, then thread will die'''

        self._on_air = False

    def run(self):
        '''Start running thread to load model for foods list from
        Open Food Facts'''

        page = 1
        pages_to_end = 1
        while pages_to_end != 0 and self._on_air:
            first_page = bool(page == 1)
            foods = self._model.download_foods(self._category, page)
            if foods:
                self._model.foods.recorded.append(foods)
                if first_page:
                    products = self._model.foods.count
                    pages_to_end = ceil(products / 20) - 1 \
                        if products >= 21 else 1
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

    def __init__(self, model, mode=Mode.SELECTED):
        super().__init__()
        self._model = model
        self._code = ""
        self._name = ""
        self._mode = mode
        self._on_air = True

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
        ''' Setter property for code'''

        self._code = value

    def __del__(self):
        self.wait()

    @pyqtSlot()
    def end_process(self):
        '''End of the loop, then thread will die'''

        self._on_air = False

    def run(self):
        '''Start to load details of product in background from Open Food
        Facts'''

        mpd = self._model.product_details
        ms = self._model.substitutes
        mpd.reset()
        if DEBUG_MODE:
            print("LoadProductDetails start searching for product with "
                  "code:", self._code, "and name:", self._name)
        self.status_message.emit("Patientez, recherche du produit "
                                 "(code {} ) en cours sur "
                                 "Open Food Facts...".format(self._code))
        food = self._model.download_product(self._code, self._name)
        if food and self._on_air:
            if self._mode == Mode.SELECTED and self._on_air:
                mpd.populate(food)
            elif self._mode == Mode.CHECKED and self._on_air:
                ms.generate_checked()
                mpd.generate_checked(food, ms.checked)
                if DEBUG_MODE:
                    print("list checked:", mpd.checked)
        else:
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


class ThreadsControler(QObject):
    '''Proxy class to control threads'''

    kill_details_show_thread = pyqtSignal()
    kill_details_checked_thread = pyqtSignal()

    def __init__(self, controler):
        super().__init__()
        self._controler = controler
        self._model = controler.model
        self._load_categories = LoadCategories(self._model, controler.database)
        self._load_product_details = {Mode.CHECKED: [], Mode.SELECTED: []}
        self._load_foods = None
        self._load_categories.start()

    def init_foods_thread(self, category):
        '''Initialize foods thread call'''

        self._load_foods = LoadFoods(self._model)
        self._controler.kill_foods_thread.connect(
            self._load_foods.end_process)
        self._load_foods.finished.connect(
            self._controler.on_load_foods_finished)
        self._load_foods.no_product_found.connect(
            self._controler.on_no_product_found)
        self._load_foods.get_a_page.connect(self._controler.on_new_food_page)
        self._load_foods.category = category
        self._load_foods.start()


    def wash_foods_thread(self):
        '''Cleaner thread for load foods'''

        if self._load_foods:
            if DEBUG_MODE:
                print("thread foods cleaning process is running")
            if self._load_foods.isRunning():
                self._load_foods.terminate()

    def init_product_details_thread(self, code, name, mode):
        '''Initialize product_details thread call'''

        self._load_product_details[mode] = LoadProductDetails(self._model,mode)
        if mode == Mode.CHECKED:
            self.kill_details_checked_thread.connect(
                self._load_product_details[mode].end_process)
        elif mode == Mode.SELECTED:
            self.kill_details_show_thread.connect(
                self._load_product_details[mode].end_process)
        self._load_product_details[mode].finished.connect(
            self._controler.on_load_product_details_finished)
        self._load_product_details[mode].status_message.connect(
            self._controler.window.on_status_message)
        self._load_product_details[mode].error_signal.connect(
            self._controler.window.on_error_message)
        self._load_product_details[mode].code = code
        self._load_product_details[mode].name = name
        self._load_product_details[mode].start()

    def wash_product_details_thread(self, mode):
        '''Clean product_details thread'''

        if self._load_product_details[mode]:
            if DEBUG_MODE:
                print("thread product details ", mode,
                      "cleaning process is running")
            if self._load_product_details[mode].isRunning():
                self._load_product_details[mode].terminate()

    @property
    def load_categories(self):
        '''Property for self._load_categories access'''

        return self._load_categories