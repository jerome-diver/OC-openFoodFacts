"""Controller for Database mode"""

import webbrowser
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QModelIndex

from model import LocalDatabaseModel
from settings import DEBUG_MODE


# noinspection PyArgumentList
class DatabaseMode(QObject):
    """ Print/record data inside local database"""

    status_message = pyqtSignal(str)

    def __init__(self, window, database):
        super().__init__()
        self._window = window
        self._database = database
        self._views = {"categories": self._window.categories_list,
                       "foods": self._window.foods_list,
                       "substitutes": self._window.substitutes_list,
                       "name": self._window.product_name,
                       "brand": self._window.product_brand,
                       "packaging": self._window.product_packaging,
                       "score": self._window.product_score,
                       "shops": self._window.product_shops,
                       "description": self._window.product_description,
                       "url": self._window.product_url,
                       "img_thumb": self._window.product_img_thumb,
                       "bg_color": self._window.get_bg_color()}
        self._model = LocalDatabaseModel(self._views, self._database)
        self._connect_signals()
        self._initialize()

    def _connect_signals(self):
        """Connect signals with slots"""

        self._views["categories"].clicked.connect(self.on_category_selected)
        self._views["foods"].clicked.connect(self.on_food_selected)
        self._views["substitutes"].clicked.connect(self.on_substitute_selected)
        self._views["url"].clicked.connect(self.on_product_url_clicked)
        self.status_message.connect(self._window.on_status_message)

    def disconnect_signals(self):
        """Disconnect signals with slots"""

        self._views["categories"].clicked.disconnect(self.on_category_selected)
        self._views["foods"].clicked.disconnect(self.on_food_selected)
        self._views["substitutes"].clicked.disconnect(self.on_substitute_selected)
        self._views["url"].clicked.disconnect(self.on_product_url_clicked)
        self.status_message.disconnect(self._window.on_status_message)

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

        index_id = self._model.categories.index(index.row(), 1)
        self._model.categories.selected = index.data()
        self._model.foods.reset()
        self._model.substitutes.reset()
        self._model.product_details.reset()
        foods = self._model.get_foods(index_id.data())
        self._model.foods.populate(foods)


    @pyqtSlot(QModelIndex)
    def on_food_selected(self, index):
        """Slot when an element of foods is selected"""

        self._model.substitutes.reset()
        self._model.product_details.reset()
        name = self._model.foods.index(index.row(), 0).data()
        code = self._model.foods.index(index.row(), 1).data()
        score = self._model.foods.index(index.row(), 2).data()
        self._model.foods.selected = (code, score, name)
        substitutes = self._model.get_substitutes(code, name)
        self._model.substitutes.populate(
            self._model.foods.selected, substitutes)


    @pyqtSlot(QModelIndex)
    def on_substitute_selected(self, index):
        """Slot when a substitute is selected"""

        code = self._model.substitutes.index(index.row(), 2).data()
        name = self._model.substitutes.index(index.row(), 0).data()
        self._model.product_details.reset()
        product_details = self._model.get_substitute_details(code, name)
        self._model.product_details.populate(product_details)

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
