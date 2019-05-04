'''OpenFoodFacts link API of openFoodFacts online with application'''

from PyQt5.QtGui import QStandardItemModel, QStandardItem
import openfoodfacts
import re

class OpenFoodFacts():

    def __init__(self, database, views):
        self._database = database
        self._views = views
        self._categories = QStandardItemModel(self._views['categories'])
        self.populate_categories()

    @property
    def categories(self):
        return self._categories

    def populate_categories(self):
        '''Return all categories by openfoodfacts module helper'''

        categories = openfoodfacts.facets.get_categories()
        for category in categories:
            regex = re.compile(r'^fr:')
            if regex.search(category["name"]):
                find = re.sub(r'^fr:', '', category["name"])
                item = QStandardItem(find)
                self._categories.appendRow(item)
