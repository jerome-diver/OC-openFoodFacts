"""Controller for OpenFoodFacts API access mode"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, \
                         QModelIndex, QItemSelection

from model import OpenFoodFacts
from . import ThreadsController, LoadCategories, Mode, Widget, \
              MixinControllers
from settings import DEBUG_MODE


class OpenFoodFactsMode(MixinControllers, QObject):
    """Print OpenFoodFacts substitutions food
    selected for category list and food list"""

    load_details_finished = pyqtSignal()
    kill_foods_thread = pyqtSignal()

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self._model = OpenFoodFacts(general_ctrl=self._general_ctrl,
                                    views=self._views)
        self._threads = ThreadsController(self)
        self._load_categories = LoadCategories(
            self._model, self._connection)
        self.initialize()

    def initialize(self):
        """Initialize the first categories populate view"""

        self._load_categories.start()

    @pyqtSlot()
    def on_load_categories_finished(self):
        """Show categories of products food from openFoodFacts
        model in view"""

        if DEBUG_MODE:
            print("=====  O p e n F o o d F a c t s M o d e  =====")
            print("let'show the wiew from threads answer")
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
            print("=====  O p e n F o o d F a c t s M o d e  =====")
            print("you are just selecting food:", self._model.foods.selected)
            print("and foods pages is", len(self._model.foods.recorded))
        self._model.substitutes.populate(self._model.foods,
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
        self.checked_start.emit("OFF_MODE")

    @property
    def threads(self):
        """Thread property access"""

        return self._threads

    @property
    def load_categories(self):
        """Property for load_categories thread access"""

        return self._load_categories
