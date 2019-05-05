'''OpenFoodFacts link API of openFoodFacts online with application'''

from PyQt5.QtGui import QStandardItemModel, QStandardItem
import openfoodfacts
import re
from collections import OrderedDict

class OpenFoodFacts():

    def __init__(self, database, views):
        self._database = database
        self._views = views
        self._categories = QStandardItemModel(self._views['categories'])
        self._foods = QStandardItemModel(self._views["foods"])
        self._foods_recorded = []
        self._substitutes = QStandardItemModel(self._views["substitutes"])
        self._substitutes.setHorizontalHeaderLabels(["Nom", "Grade"])
        self.populate_categories()

    @property
    def categories(self):
        return self._categories

    @property
    def foods(self):
        return self._foods

    @property
    def substitutes(self):
        return self._substitutes

    def populate_categories(self):
        '''Return all categories inside list categories view
        by openfoodfacts module helper'''

        self._categories.removeRows(0, self.foods.rowCount())
        categories = openfoodfacts.facets.get_categories()
        sorted_categories = sorted(categories, key = lambda kv: kv["name"])
        for category in sorted_categories:
            is_fr = re.match(r'^fr:', category["name"])
            is_latin_chars = re.match(r'[0-9a-zA-z\s]', category["name"])
            if is_fr and is_latin_chars:
                find = re.sub(r'^fr:', '', category["name"])
                item = QStandardItem(find)
                self._categories.appendRow(item)

    def populate_foods(self, category):
        '''Return the list wiew of foods for give category string
        with openfoodfacts library helper'''

        def get_food_item(this, food, key):
            '''Define item'''

            item = QStandardItem("undefined")
            if food[key].strip().isspace() \
                    or food[key] == '':
                print(food)
            else:
                item = QStandardItem(food[key].strip())
            this._foods.appendRow(item)

        def normalize_foods_products(foods_products):
            '''Normalize data products content by adding missing keys'''

            for food in foods_products:
                if "product_name_fr" not in food:
                    food["product_name_fr"] = food["product_name"]


        self.foods.removeRows(0, self.foods.rowCount())
        foods = openfoodfacts.products.advanced_search(
            {   "search_terms" : category,
                "search_tag" : "categories",
                "country" : "france" }
        )
        normalize_foods_products(foods["products"])
        sorted_foods = sorted(foods["products"],
                              key = lambda kv: kv["product_name_fr"])
        self._foods_recorded = sorted_foods
        for food in sorted_foods:
            if "product_name_fr" in food:
                get_food_item(self, food, "product_name_fr")
            else:
                get_food_item(self, food, "product_name")


    def populate_substitutes(self, food):
        '''Return the list of possible substitution products inside
        substitutes list view'''

        self.substitutes.removeRows(0, self.substitutes.rowCount())
        for food in self._foods_recorded:
            item_name = QStandardItem(food["product_name_fr"])
            item_name.setCheckable(True)
            item_grade = QStandardItem("{}".format(food[
                                           "nutrition_grades_tags"][0]))
            self._substitutes.appendRow([item_name, item_grade])


