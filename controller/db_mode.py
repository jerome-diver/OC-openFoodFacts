"""Controller for Database mode"""

import webbrowser
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, \
                         QModelIndex, QItemSelection

from . import Widget, Mode, ControllerSlots
from model import LocalDatabaseModel
from settings import DEBUG_MODE


# noinspection PyArgumentList
class DatabaseMode(QObject):
    """ Print/record data inside local database"""

    status_message = pyqtSignal(str)
    checked_start = pyqtSignal()

    def __init__(self, general_ctrl):
        super().__init__()
        self._general_ctrl = general_ctrl
        self._window = general_ctrl.window
        self._authenticate = general_ctrl.authenticate
        self._connection = self._authenticate.user_connection
        self._flags = {"product": True,
                       "internet": True,
                       "call_mode": Mode.SELECTED}
        self._views = {"categories": self._window.categories_list,
                       "foods": self._window.foods_list,
                       "substitutes": self._window.substitutes_list,
                       "code": self._window.product_code,
                       "name": self._window.product_name,
                       "brand": self._window.product_brand,
                       "packaging": self._window.product_packaging,
                       "score": self._window.product_score,
                       "shops": self._window.product_shops,
                       "description": self._window.product_description,
                       "url": self._window.product_url,
                       "img_thumb": self._window.product_img_thumb,
                       "bg_color": self._window.get_bg_color()}
        self._model = LocalDatabaseModel(general_ctrl, self._views)
        self._slots = ControllerSlots(general_ctrl, self)
        self._initialize()

    def _initialize(self):
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


    @pyqtSlot(QModelIndex)
    def on_substitute_selected(self, index):
        """Slot when a substitute is selected"""

        code = self._model.substitutes.index(index.row(), 2).data()
        self._model.product_details.reset()
        product_details = self._model.get_product_details(code)
        self._model.product_details.populate(product_details)
        self._window.show_product_details(
            self._model.product_details.models)

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
    def connection(self):
        """connection property access"""

        return self._connection

    @property
    def window(self):
        """Window access property"""

        return self._window

    @property
    def views(self):
        """Views property access"""

        return self._views

    @property
    def flags(self):
        """Property for flags access"""

        return self._flags

    @property
    def slots(self):
        """Property for slots access"""

        return self._slots

