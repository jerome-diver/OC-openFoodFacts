"""Controller for OpenFoodFacts API access mode"""

import webbrowser
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, \
                         QModelIndex, QItemSelection
from model import OpenFoodFacts
from controller import ThreadsControler, Mode, Widget
from view import Messenger
from settings import DEBUG_MODE


class OpenFoodFactsMode(QObject):
    """Print OpenFoodFacts substitutions food
    selected for category list and food list"""

    status_message = pyqtSignal(str)
    checked_start = pyqtSignal()
    load_details_finished = pyqtSignal()
    kill_foods_thread = pyqtSignal()

    def __init__(self, window, database):
        super().__init__()
        self._window = window
        self._database = database
        self._views = {"categories": self._window.categories_list,
                       "foods": self._window.foods_list,
                       "substitutes": self._window.substitutes_list,
                       "name" : self._window.product_name,
                       "brand" : self._window.product_brand,
                       "packaging" : self._window.product_packaging,
                       "code": self._window.product_code,
                       "score" : self._window.product_score,
                       "shops" : self._window.product_shops,
                       "description" : self._window.product_description,
                       "url" : self._window.product_url,
                       "img_thumb" : self._window.product_img_thumb,
                       "bg_color": self._window.get_bg_color()}
        self._model = OpenFoodFacts(self._views, database)
        self._threads = ThreadsControler(self)
        self._flags = {"product": True,
                       "internet": True,
                       "call_mode": Mode.SELECTED}
        self._messenger = Messenger(self, self._flags)
        self.connect_signals()


    def connect_signals(self):
        """Connect signals to slots for concerned controller"""

        self._views["categories"].clicked.connect(self.on_category_selected)
        self._views["foods"].clicked.connect(self.on_food_selected)
        self._views["substitutes"].selectionModel().selectionChanged.connect(
            self.on_substitute_selection_changed)
        self._model.substitutes.itemChanged.connect(self.on_substitute_checked)
        self._views["url"].clicked.connect(self.on_product_url_clicked)
        self._threads.load_categories.finished.connect(
            self.on_load_categories_finished)
        self._model.internet_access.connect(self.on_internet_access)
        self.status_message.connect(self._window.on_status_message)
        self._views["categories"].clicked.connect(
            self._messenger.on_category_selected)
        self._views["foods"].clicked.connect(
            self._messenger.on_food_selected)
        self._views["substitutes"].selectionModel().selectionChanged.connect(
            self._messenger.on_substitute_selection_changed)
        self._model.substitutes.itemChanged.connect(
            self._messenger.on_substitute_checked)
        self._threads.load_categories.finished.connect(
            self._messenger.on_load_categories_finished)
        self._model.internet_access.connect(
            self._messenger.on_internet_access)
        self._messenger.status_message.connect(self._window.on_status_message)

    def disconnect_signals(self):
        """Disconnect signals to slots for concerned controller"""

        self._views["categories"].clicked.disconnect(self.on_category_selected)
        self._views["foods"].clicked.disconnect(self.on_food_selected)
        self._views["substitutes"].selectionModel().selectionChanged.disconnect(
            self.on_substitute_selection_changed)
        self._model.substitutes.itemChanged.disconnect(self.on_substitute_checked)
        self._views["url"].clicked.disconnect(self.on_product_url_clicked)
        self._threads.load_categories.finished.disconnect(
            self.on_load_categories_finished)
        self._model.internet_access.disconnect(self.on_internet_access)
        self.status_message.disconnect(self._window.on_status_message)

    @pyqtSlot()
    def on_load_categories_finished(self):
        """Show categories of products food
        from openFoodFacts model in view"""

        self._window.show_categories(self._model.categories)

    @pyqtSlot()
    def on_load_foods_finished(self):
        """Show food's products from Open Food Facts"""

        if DEBUG_MODE:
            print("End process to load foods")

    @pyqtSlot(int, int)
    def on_new_food_page(self, page, total):
        """Reload the view for new page added"""

        if page == 1:
            self._window.show_foods(self._model.foods)
        if self._model.foods.selected:
            self._model.substitutes.populate(self._model.foods.selected,
                                             self._model.foods.recorded,
                                             page - 1, False)

    @pyqtSlot()
    def on_load_product_details_finished(self):
        """Show details of product from Open Food Facts"""

        if self._flags["call_mode"] is Mode.SELECTED:
            self._window.show_product_details(self._model.product_details.models)
        elif self._flags["call_mode"] is Mode.CHECKED:
            self.load_details_finished.emit()

    @pyqtSlot()
    def on_no_product_found(self):
        """When no product found for category selected happening..."""

        self._model.reset_models((Widget.FOODS,
                                  Widget.SUBSTITUTES,
                                  Widget.DETAILS))
        self._window.reset_views((Widget.FOODS,
                                  Widget.SUBSTITUTES,
                                  Widget.DETAILS))
        self._flags["product"] = False

    @pyqtSlot(bool)
    def on_internet_access(self, status):
        """When no internet access is happening..."""

        self._flags["internet"] = status
        self._window.openfoodfacts_mode.setEnabled(status)

    @pyqtSlot(QModelIndex)
    def on_category_selected(self, index):
        """Slot for next action on clicked category selection from
        category list view"""

        self._flags["product"] = True
        self.kill_foods_thread.emit()
        self._model.reset_models((Widget.FOODS,
                                  Widget.SUBSTITUTES,
                                  Widget.DETAILS))
        self._window.reset_views((Widget.FOODS,
                                  Widget.SUBSTITUTES,
                                  Widget.DETAILS))
        id = self._model.categories.index(index.row(), 1).data()
        self._model.foods.category_id = id
        self._threads.init_foods_thread(index.data())

    @pyqtSlot(QModelIndex)
    def on_food_selected(self, index):
        """Slot for next action on clicked foods selection from
        foods list view"""

        self._model.reset_models((Widget.SUBSTITUTES,
                                  Widget.DETAILS))
        self._window.reset_views((Widget.SUBSTITUTES,
                                  Widget.DETAILS))
        name = index.data()
        code = self._model.foods.index(index.row(), 1).data()
        score = self._model.foods.index(index.row(), 2).data()
        self._model.foods.selected = (code, score, name)
        if DEBUG_MODE:
            print("you are just selecting food:", self._model.foods.selected)
            print("and foods pages is", len(self._model.foods.recorded))
        self._model.substitutes.populate(self._model.foods.selected,
                                         self._model.foods.recorded)
        self._threads.init_product_details_thread(code, name, Mode.GET)
        self.show_substitutes()

    def show_substitutes(self):
        """Just show substitute products list"""

        self._window.show_substitutes(self._model.substitutes)

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_substitute_selection_changed(self, selected, deselected):
        """Load details from new selection of substitutes table view"""

        if selected.indexes():
            index_select = selected.indexes()[0]
            self._flags["call_mode"] = Mode.SELECTED
            sub_model = self._views["substitutes"].model()
            code = sub_model.index(index_select.row(), 2).data()
            name = sub_model.index(index_select.row(), 0).data()
            self._threads.init_product_details_thread(code, name,
                                                      Mode.SELECTED)

    @pyqtSlot('QStandardItem*')
    def on_substitute_checked(self, item):
        """Load, from checkbox (substitutes table view) selected, products
        details"""

        self._flags["call_mode"] = Mode.CHECKED
        index = self._model.substitutes.indexFromItem(item)
        code = self._model.substitutes.index(index.row(), 2).data()
        name = self._model.substitutes.index(index.row(), 0).data()
        self._threads.init_product_details_thread(code, name, Mode.CHECKED)
        self.checked_start.emit()

    @pyqtSlot()
    def on_product_url_clicked(self):
        """Go to url"""

        url = self._model.product_details.models["url"]
        webbrowser.open(url)

    @property
    def model(self):
        """Return model property for OpenFoodFacts instance model"""

        return self._model

    @property
    def database(self):
        """Database property access"""

        return self._database

    @property
    def window(self):
        """Window access property"""

        return self._window
