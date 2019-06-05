"""Module For threads loaders to run Open Food Facts request call on
background to not freeze application"""

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, \
                         QThread, QRunnable, QThreadPool

from settings import DEBUG_MODE
from enumerator import Mode
from model import OpenFoodFacts, LocalDatabase


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


class ProductDetailsSignals(QObject):
    """LoadProductDetails QRunnable has threads there:"""

    error_signal = pyqtSignal(str)
    status_message = pyqtSignal(str)
    finished = pyqtSignal(Mode)

    def __init__(self, thread):
        super().__init__()
        self._thread = thread

    @pyqtSlot(Mode)
    def end_process(self, mode):
        """End of the loop, then thread will die"""

        if self._thread.mode == mode :
            self._thread.on_air = False


class LoadProductDetails(QRunnable):
    """Load product selected from substitutes list to create model
    for details"""

    count = 0
    mode_checked = 0
    mode_selected_food = 0
    mode_selected_substitute = 0

    def __init__(self, model, mode=Mode.SELECTED_FOOD):
        super().__init__()
        self._model = model
        self._caller = None
        self._index = None
        self._mode = mode
        if mode == Mode.CHECKED:
            LoadProductDetails.mode_checked += 1
        elif mode == Mode.SELECTED_FOOD:
            LoadProductDetails.mode_selected_food += 1
        elif mode == Mode.SELECTED_SUBSTITUTE:
            LoadProductDetails.mode_selected_substitute += 1
        self._on_air = True
        self._signals = ProductDetailsSignals(self)
        LoadProductDetails.count += 1
        if DEBUG_MODE:
            print("======  L o a d P r o d u c t D e t a i l s  (start n°{"
                  "})======".format(LoadProductDetails.count))

    def __del__(self):
        """At end time"""

        if self._on_air == False:
            LoadProductDetails.count -= self.mode_selected_food \
                if self._mode is Mode.SELECTED_FOOD \
                else self.mode_selected_substitute
        else:
            LoadProductDetails.count -= 1
        if self._mode == Mode.CHECKED:
            LoadProductDetails.mode_checked -= 1
        elif self._mode == Mode.SELECTED_FOOD:
            LoadProductDetails.mode_selected_food -= 1
        elif self._mode == Mode.SELECTED_SUBSTITUTE:
            LoadProductDetails.mode_selected_substitute -= 1
        if DEBUG_MODE:
            print("======  L o a d P r o d u c t D e t a i l s  ======")
            print("======  END Checked n° {}  ======".format(
                LoadProductDetails.mode_checked))
            print("======  END Selected n° {}  ======".format(
                LoadProductDetails.mode_selected_food))
            print("======  END Selected n° {}  ======".format(
                LoadProductDetails.mode_selected_substitute))
            print("=====  Total in life: ", LoadProductDetails.count)

    def run(self):
        """Start to load details of product in background from Open Food
        Facts"""

        mpd = self._model.product_details
        mf = self._model.foods
        ms = self._model.substitutes
        code = self._caller.index(self._index.row(), 2).data()
        name = self._caller.index(self._index.row(), 0).data()
        if DEBUG_MODE:
            print("===== L o a d P r o d u c t D e t a i l s  (thread) =====")
        details = None
        try:
            if isinstance(self._model, OpenFoodFacts):
                details = self._model.download_product(code, name)
            if isinstance(self._model, LocalDatabase):
                details = self._model.get_product_details(code)
            if details and self._on_air:
                if self._mode == Mode.SELECTED_FOOD and self._on_air:
                    mpd.populate(details)
                    mf.selected_details = details
                elif self._mode == Mode.SELECTED_SUBSTITUTE and self._on_air:
                    mpd.populate(details)
                elif self._mode == Mode.CHECKED and self._on_air:
                    to_add = ms.update_checked(self._index, code)
                    mpd.update_checked(details, to_add)
        except:
            self._signals.error_signal.emit("Hélas, il n'y a aucun détail "
                                            "enregistré pour ce produit")
        else:
            self._signals.status_message.emit("Aucun détail exploitable ici "
                                              "n'est fourni")
        finally:
            if self._on_air:
                self._signals.finished.emit(self._mode)
            else:
                self._signals.finished.emit(Mode.KILLED)

    @property
    def caller(self):
        """Return property for product name substitute"""

        return self._caller

    @caller.setter
    def caller(self, model):
        """Setter property for name of substitute product"""

        self._caller = model

    @property
    def index(self):
        """Return property for code product substitute"""

        return self._index

    @index.setter
    def index(self, idx):
        """ Setter property for code"""

        self._index = idx

    @property
    def signals(self):
        """Property for own signals to be connected"""

        return self._signals

    @property
    def mode(self):
        """mMde property"""

        return self._mode

    @property
    def on_air(self):
        """On_air property"""

        return self._on_air

    @on_air.setter
    def on_air(self, value):
        """Setter for on_air"""

        self._on_air = value

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

    kill_details_threads= pyqtSignal(Mode)

    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self._model = controller.model
        self._load_foods = None
        self._product_details_checked_pool = QThreadPool()
        self._product_details_selected_pool = QThreadPool()
        self._product_details_checked_pool.setMaxThreadCount(16)
        self._product_details_selected_pool.setMaxThreadCount(16)

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

    def init_product_details_thread(self, model_caller, index, mode):
        """Initialize product_details thread call"""

        load_product_details = LoadProductDetails(self._model, mode)
        self.kill_details_threads.connect(
            load_product_details.signals.end_process)
        load_product_details.signals.finished.connect(
            self._controller.on_load_product_details_finished)
        load_product_details.signals.finished.connect(
            self._controller.messenger.on_load_product_details_finished)
        load_product_details.signals.status_message.connect(
            self._controller.window.on_status_message)
        load_product_details.signals.error_signal.connect(
            self._controller.window.on_error_message)
        load_product_details.caller = model_caller
        load_product_details.index = index
        if mode is Mode.CHECKED:
            self._product_details_checked_pool.start(load_product_details)
        else:
            self._product_details_selected_pool.start(load_product_details)

    def wash_product_details_thread(self, mode):
        """Clean product_details thread"""

        if self._load_product_details[mode]:
            if DEBUG_MODE:
                print("thread product details ", mode,
                      "cleaning process is running")
            if self._load_product_details[mode].isRunning():
                self._load_product_details[mode].terminate()

