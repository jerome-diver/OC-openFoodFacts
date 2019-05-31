"""Module For threads loaders to run Open Food Facts request call on
background to not freeze application"""

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, \
                         QThread

from settings import DEBUG_MODE
from enumerator import Mode


class LoadCategories(QThread):
    """Load Categories model in background process to not freeze
    thz application"""

    def __init__(self, model, connection):
        super().__init__()
        self._model = model
        self._connection = connection

    def __del__(self):
        self.wait()

    def run(self):
        """Start running the thread for populate model of Open Food Facts
        categories list from local database or from Open Food Facts API
        online"""

        categories = []
        request = "SELECT id, name FROM categories ORDER BY name;"
        for row in  self._connection.ask_request(request):
            categories.append(row)
        if not categories:
            categories = self._model.download_categories()
        self._model.categories.populate(categories)


class LoadFoods(QThread):
    """Load foods model in background to not freeze application"""

    get_a_page = pyqtSignal(int, int)
    no_product_found = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self._model = model
        self._category = ''
        self._on_air = True

    def __del__(self):
        self.wait()

    @pyqtSlot()
    def end_process(self):
        """End of the loop, then thread will die"""

        self._on_air = False

    def run(self):
        """Start running thread to load model for foods list from
        Open Food Facts"""

        page = 1
        have_more_product = True
        self._model.foods.recorded = []
        while have_more_product and self._on_air:
            first_page = bool(page == 1)
            foods = self._model.download_foods(self._category, page)
            if foods:
                have_more_product = bool(len(foods) >= 21)
                if DEBUG_MODE:
                    print("===== L o a d F o o d s  (thread)  =====")
                    print("there is foods to add...")
                self._model.foods.recorded.append(foods)
                self._model.foods.populate(foods, first_page)
                self.get_a_page.emit(page, "?")
            else:
                have_more_product = False
                self.no_product_found.emit()
            page += 1

    @property
    def category(self):
        """Return property of category name"""

        return self._category

    @category.setter
    def category(self, value):
        """Setter for property of category name"""

        self._category = value


class LoadProductDetails(QThread):
    """Load product selected from substitutes list to create model
    for details"""

    error_signal = pyqtSignal(str)
    status_message = pyqtSignal(str)

    def __init__(self, model, mode=Mode.SELECTED):
        super().__init__()
        self._model = model
        self._code = ""
        self._name = ""
        self._mode = mode
        self._on_air = True

    def __del__(self):
        self.wait()

    @pyqtSlot()
    def end_process(self):
        """End of the loop, then thread will die"""

        self._on_air = False

    def run(self):
        """Start to load details of product in background from Open Food
        Facts"""

        mpd = self._model.product_details
        mf = self._model.foods
        ms = self._model.substitutes
        mpd.reset()
        if DEBUG_MODE:
            print("===== L o a d P r o d u c t D e t a i l s  (thread) =====")
            print("LoadProductDetails start searching for product")
            print("with code:", self._code, "and name:", self._name)
        self.status_message.emit("Patientez, recherche du produit "
                                 "(code {} ) en cours sur "
                                 "Open Food Facts...".format(self._code))
        food = self._model.download_product(self._code, self._name)
        if food and self._on_air:
            if self._mode == Mode.GET and self._on_air:
                mpd.populate(food)
                mf.selected_details = food
            elif self._mode == Mode.SELECTED and self._on_air:
                mpd.populate(food)
            elif self._mode == Mode.CHECKED and self._on_air:
                ms.generate_checked()
                mpd.generate_checked(food, ms.checked)
                if DEBUG_MODE:
                    print("===== L o a d P r o d u c t D e t a i l s  "
                          "(thread) =====")
                    print("list checked:", mpd.checked)
        else:
            self.error_signal.emit("Hélas, il n'y a aucun détail enregistré "
                                   "pour ce code produit")
            self.status_message.emit("Aucun détail cohérent n'est fourni")

    @property
    def name(self):
        """Return property for product name substitute"""

        return self._name

    @name.setter
    def name(self, value):
        """Setter property for name of substitute product"""

        self._name = value

    @property
    def code(self):
        """Return property for code product substitute"""

        return self._code

    @code.setter
    def code(self, value):
        """ Setter property for code"""

        self._code = value


class UpdateCategories(QThread):
    """Load categories from Open Food Facts in background in categories
    table of the Open Food Facts_substitutes database"""

    def __init__(self, connection, off_model):
        super().__init__()
        self._connection = connection
        self._off_model = off_model

    def __del__(self):
        self.wait()

    def run(self):
        """Start thread job"""

        if DEBUG_MODE:
            print("=====  U p d a t e C a t e g o r i e s  (thread)  =====")
            print("start to update categories table from OFF categories")
        categories = self._off_model.download_categories()
        if categories:
            self._connection.update_categories(categories)
        if DEBUG_MODE:
            print("End of update categories table from thread")


class ThreadsController(QObject):
    """Proxy class to control threads"""

    kill_details_show_thread = pyqtSignal()
    kill_details_checked_thread = pyqtSignal()
    kill_details_get_thread = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self._model = controller.model
        self._load_product_details = {Mode.CHECKED: [],
                                      Mode.SELECTED: [],
                                      Mode.GET: []}
        self._load_foods = None
        #self._load_categories.start()

    def init_foods_thread(self, category):
        """Initialize foods thread call"""

        self._load_foods = LoadFoods(self._model)
        self._controller.kill_foods_thread.connect(
            self._load_foods.end_process)
        self._load_foods.finished.connect(
            self._controller.on_load_foods_finished)
        self._load_foods.no_product_found.connect(
            self._controller.on_no_product_found)
        self._load_foods.get_a_page.connect(self._controller.on_new_food_page)
        self._load_foods.category = category
        self._load_foods.start()

    def wash_foods_thread(self):
        """Cleaner thread for load foods"""

        if self._load_foods:
            if DEBUG_MODE:
                print("=====  T h r e a d s C o n t r o l l e r  =====")
                print("thread foods cleaning process is running")
            if self._load_foods.isRunning():
                self._load_foods.terminate()

    def init_product_details_thread(self, code, name, mode):
        """Initialize product_details thread call"""

        self._load_product_details[mode] = LoadProductDetails(self._model,mode)
        if mode == Mode.CHECKED:
            self.kill_details_checked_thread.connect(
                self._load_product_details[mode].end_process)
        elif mode == Mode.SELECTED:
            self.kill_details_show_thread.connect(
                self._load_product_details[mode].end_process)
        elif mode == Mode.GET:
            self.kill_details_get_thread.connect(
                self._load_product_details[mode].end_process)
        self._load_product_details[mode].finished.connect(
            self._controller.on_load_product_details_finished)
        self._load_product_details[mode].status_message.connect(
            self._controller.window.on_status_message)
        self._load_product_details[mode].error_signal.connect(
            self._controller.window.on_error_message)
        self._load_product_details[mode].code = code
        self._load_product_details[mode].name = name
        self._load_product_details[mode].start()

    def wash_product_details_thread(self, mode):
        """Clean product_details thread"""

        if self._load_product_details[mode]:
            if DEBUG_MODE:
                print("thread product details ", mode,
                      "cleaning process is running")
            if self._load_product_details[mode].isRunning():
                self._load_product_details[mode].terminate()

