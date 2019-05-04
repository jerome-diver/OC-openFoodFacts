'''Controller for OpenFoodFacts API access mode'''

from model import OpenFoodFacts
import requests


class OpenFoodFactsMode():
    '''Print OpenFoodFacts substitutions food 
    selected for category list and food list'''

    def __init__(self, window, database):
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

    def show_categories(self):
        '''Show categories of products food
        from openFoodFacts model in view'''

        self._window.show_categories(self._model.categories)

