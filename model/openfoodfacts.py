'''OpenFoodFacts link API of openFoodFacts online with application'''

from PyQt5.QtGui import QStandardItemModel, QStandardItem
import openfoodfacts
import re

class OpenFoodFacts():

    def __init__(self, database, views):
        self._database = database
        self._views = views
        self._categories = QStandardItemModel(self._views['categories'])
        self._foods = QStandardItemModel(self._views["foods"])
        self.populate_categories()

    @property
    def categories(self):
        return self._categories

    @property
    def foods(self):
        return self._foods

    def populate_categories(self):
        '''Return all categories inside list categories view
        by openfoodfacts module helper'''

        self._categories.removeRows(0, self.foods.rowCount())
        categories = openfoodfacts.facets.get_categories()
        for category in categories:
            is_fr = re.match(r'^fr:', category["name"])
            is_latin_chars = re.match(r'[0-9a-zA-z\s]', category["name"])
            if is_fr and is_latin_chars:
                find = re.sub(r'^fr:', '', category["name"])
                item = QStandardItem(find)
                self._categories.appendRow(item)

    def populate_foods(self, category):
        '''Return the list wiew of foods for give category string
        with openfoodfacts library helper'''

        self.foods.removeRows(0, self.foods.rowCount())
        foods = openfoodfacts.products.advanced_search(
            {   "search_terms" : category,
                "search_tag" : "categories",
                "country" : "france" }
        )
        for food in foods["products"]:
            item = QStandardItem("undefined")
            if "product_name_fr" in food:
                if food["product_name_fr"].strip().isspace() \
                        or food["product_name_fr"] == '':
                    print(food)
                else:
                    item = QStandardItem(food["product_name_fr"].strip())
            else:
                if food["product_name"].strip().isspace() \
                        or food["product_name"] == '':
                    print(food)
                else:
                    item = QStandardItem(food["product_name"].strip())
            self._foods.appendRow(item)