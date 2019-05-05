'''Controller for OpenFoodFacts API access mode'''

from model import OpenFoodFacts
from PyQt5.QtCore import QObject, pyqtSlot, QModelIndex


class OpenFoodFactsMode(QObject):
    '''Print OpenFoodFacts substitutions food 
    selected for category list and food list'''

    def __init__(self, window, database):
        super().__init__()
        self._window = window
        self._database = database
        self.views = { "categories": self._window.categories_list,
                       "foods": self._window.foods_list,
                       "substitutes": self._window.substitutes_list,
                       "name" : self._window.substitute_name,
                       "description" : self._window.substitute_description,
                       "shop" : self._window.substitute_shop,
                       "url" : self._window.substitute_url,
                       "score" : self._window.substitute_score
                      }
        self._model = OpenFoodFacts(database, self.views)
        self.show_categories()
        self.connect_signals()

    def connect_signals(self):
        '''Let's connect signals to slots for concerned controller'''

        self._window.categories_list.clicked.connect(
            self.on_category_selected)

    def show_categories(self):
        '''Show categories of products food
        from openFoodFacts model in view'''

        self._window.show_categories(self._model.categories)

    pyqtSlot(QModelIndex)
    def on_category_selected(self, index):
        '''Slot for next action on clicked category selection from
        category list view'''

        category_selected = index.data()
        self._model.populate_foods(category_selected)
        self._window.show_foods(self._model.foods)