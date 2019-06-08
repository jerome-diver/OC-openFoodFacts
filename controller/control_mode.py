"""Controller for OpenFoodFacts API access mode"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, \
                         QModelIndex, QItemSelection

from . import MixinControllers
from enumerator import Mode, Widget
from settings import DEBUG_MODE


class OpenFoodFactsMode(MixinControllers, QObject):
    """Print OpenFoodFacts substitutions food
    selected for category list and food list"""

    kill_foods_thread = pyqtSignal()

    def __init__(self, **kargs):
        super().__init__(**kargs)
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
        sub_model = self._model.foods
        name = sub_model.index(index.row(), 0).data()
        score = sub_model.index(index.row(), 1).data()
        code = sub_model.index(index.row(), 2).data()
        sub_model.selected = (code, score, name)
        if DEBUG_MODE:
            print("=====  O p e n F o o d F a c t s M o d e  =====")
            print("you are just selecting food:", self._model.foods.selected)
            print("and foods pages is", len(self._model.foods.recorded))
        self._model.substitutes.populate(sub_model, sub_model.recorded)
        self._last = {
            "selection": Mode.SELECTED_FOOD,
            "code": sub_model.index(index.row(), 2).data() }
        self._threads.init_product_details_thread(sub_model, index,
                                                  Mode.SELECTED_FOOD)
        self.show_substitutes()

    def show_substitutes(self):
        """Just show substitute products list"""

        self._window.show_substitutes(self._model.substitutes)

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_substitute_selection_changed(self, selected, deselected):
        """Load details from new selection of substitutes table view"""

        if selected.indexes():
            self._model.reset_models((Widget.DETAILS,))
            self._window.reset_views((Widget.DETAILS,))
            index_select = selected.indexes()[0]
            sub_model = self._views["substitutes"].model()
            self._last = {
                "selection": Mode.SELECTED_SUBSTITUTE,
                "code": sub_model.index(index_select.row(), 2).data() }
            self._threads.init_product_details_thread(sub_model,
                                                      index_select,
                                                      Mode.SELECTED_SUBSTITUTE)

    @pyqtSlot('QStandardItem*')
    def on_substitute_checked(self, item):
        """Load, from checkbox (substitutes table view) selected, products
        details"""

        sub_model = self._model.substitutes
        index = sub_model.indexFromItem(item)
        code = sub_model.index(index.row(), 2).data()
        if sub_model.update_checked(item, code):
            self._threads.init_product_details_thread(sub_model,
                                                      index,
                                                      Mode.CHECKED)
        else:
            # clear thread from pool and/or send a kill signal
            pass
        self.checked_start.emit()

    @property
    def threads(self):
        """Thread property access"""

        return self._threads

    @property
    def load_categories(self):
        """Property for load_categories thread access"""

        return self._load_categories


class DatabaseMode(MixinControllers, QObject):
    """ Print/record data inside local database"""

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.initialize()

    def initialize(self):
        """Show categories first"""

        categories = self._model.get_categories()
        if DEBUG_MODE:
            print("get", len(categories), "categories found in database")
        self._model.categories.populate(categories)
        self._window.show_categories(self._model.categories)

    @pyqtSlot(QModelIndex)
    def on_category_selected(self, index):
        """Slot when an element of categories list is selected"""

        self._model.reset_models((Widget.FOODS,
                                  Widget.SUBSTITUTES,
                                  Widget.DETAILS))
        self._window.reset_views((Widget.FOODS,
                                  Widget.SUBSTITUTES,
                                  Widget.DETAILS))
        id = self._model.categories.index(index.row(), 1).data()
        self._model.foods.category_id = id
        foods = self._model.get_foods(id)
        self._model.foods.populate(foods)
        self._window.show_foods(self._model.foods)
        self._messenger.on_load_foods_finished()

    @pyqtSlot(QModelIndex)
    def on_food_selected(self, index):
        """Slot when an element of foods is selected"""

        self._model.reset_models((Widget.SUBSTITUTES,
                                  Widget.DETAILS))
        self._window.reset_views((Widget.SUBSTITUTES,
                                  Widget.DETAILS))
        sub_model = self._model.foods
        name = sub_model.index(index.row(), 0).data()
        score = sub_model.index(index.row(), 1).data()
        code = sub_model.index(index.row(), 2).data()
        sub_model.selected = (code, score, name)
        substitutes = self._model.get_substitutes(code)
        self._model.substitutes.populate(sub_model, substitutes)
        self._last = {
            "selection": Mode.SELECTED_FOOD,
            "code": sub_model.index(index.row(), 2).data() }
        self._threads.init_product_details_thread(sub_model, index,
                                                  Mode.SELECTED_FOOD)
        self._window.show_substitutes(self._model.substitutes)

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_substitute_selection_changed(self, selected, deselected):
        """Load details from new selection of substitutes table view"""

        if selected.indexes():
            self._model.reset_models((Widget.DETAILS,))
            self._window.reset_views((Widget.DETAILS,))
            index_select = selected.indexes()[0]
            sub_model = self._model.substitutes
            self._last = {
                "selection": Mode.SELECTED_SUBSTITUTE,
                "code": sub_model.index(index_select.row(), 2).data() }
            self._threads.init_product_details_thread(sub_model,
                                                      index_select,
                                                      Mode.SELECTED_SUBSTITUTE)

    @pyqtSlot('QStandardItem*')
    def on_substitute_checked(self, item):
        """Load, from checkbox (substitutes table view) selected,
        products details"""

        index = self._model.substitutes.indexFromItem(item)
        ms = self._model.substitutes
        code = ms.index(index.row(), 2).data()
        if ms.update_checked(item, code):
            self._threads.init_product_details_thread(ms,
                                                      index,
                                                      Mode.CHECKED)
        else:
            # clear thread from pool and/or send a kill signal
            pass
        self.checked_start.emit()

