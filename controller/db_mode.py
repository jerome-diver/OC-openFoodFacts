"""Controller for Database mode"""

from PyQt5.QtCore import QObject, pyqtSlot, \
                         QModelIndex, QItemSelection

from . import Widget, Mode, MixinControllers
from settings import DEBUG_MODE


# noinspection PyArgumentList
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

    @pyqtSlot(QModelIndex)
    def on_food_selected(self, index):
        """Slot when an element of foods is selected"""

        self._model.substitutes.reset()
        self._model.product_details.reset()
        name = self._model.foods.index(index.row(), 0).data()
        code = self._model.foods.index(index.row(), 1).data()
        score = self._model.foods.index(index.row(), 2).data()
        self._model.foods.selected = (code, score, name)
        substitutes = self._model.get_substitutes(code)
        self._model.substitutes.populate(self._model.foods, substitutes)
        product_details = self._model.get_product_details(code)
        self._model.product_details.populate(product_details)
        self._window.show_substitutes(self._model.substitutes)

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_substitute_selection_changed(self, selected, deselected):
        """Load details from new selection of substitutes table view"""

        if selected.indexes():
            index_select = selected.indexes()[0]
            self._flags["call_mode"] = Mode.SELECTED
            sub_model = self._views["substitutes"].model()
            code = sub_model.index(index_select.row(), 2).data()
            product_details = self._model.get_product_details(code)
            self._model.product_details.populate(product_details)
            self._window.show_product_details(
                self._model.product_details.models)

    @pyqtSlot('QStandardItem*')
    def on_substitute_checked(self, item):
        """Load, from checkbox (substitutes table view) selected,
        products details"""

        self._flags["call_mode"] = Mode.CHECKED
        index = self._model.substitutes.indexFromItem(item)
        code = self._model.substitutes.index(index.row(), 2).data()
        mpd = self._model.product_details
        ms = self._model.substitutes
        ms.generate_checked()
        product_details = self._model.get_product_details(code)
        mpd.generate_checked(product_details, ms.checked)
        self.checked_start.emit("LOCAL_DB_MODE")

