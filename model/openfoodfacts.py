'''OpenFoodFacts link API of openFoodFacts online with application'''

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QObject, pyqtSlot, QModelIndex
import openfoodfacts
import re
from collections import OrderedDict

class OpenFoodFacts(QObject):
    '''Model for Open Food Facts data requests'''

    def __init__(self, database, views):
        super().__init__()
        self._database = database
        self._views = views
        self._categories = QStandardItemModel(self._views['categories'])
        self._foods = QStandardItemModel(self._views["foods"])
        self._foods_recorded = []
        self._substitutes = QStandardItemModel(self._views["substitutes"])
        self._substitutes.setHorizontalHeaderLabels(["Nom", "Grade", "Code"])
        self._details = { "name": self._views["name"],
                          "description" : self._views["description"],
                          "shops" : QStandardItemModel(self._views["shops"]),
                          "url" : self._views["url"],
                          "score" : self._views["score"]
                          }

    @property
    def categories(self):
        return self._categories

    @property
    def foods(self):
        return self._foods

    @property
    def substitutes(self):
        return self._substitutes

    @property
    def details(self):
        return self._details

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
        foods_grade_sorted = sorted(self._foods_recorded,
                                    key = lambda kv:
                                    kv["nutrition_grades_tags"][0])
        for _food in foods_grade_sorted:
            if _food["product_name_fr"] != food \
                    and _food["nutrition_grades_tags"][0] != "not-applicable":
                item_name = QStandardItem(_food["product_name_fr"])
                item_name.setCheckable(True)
                item_grade = QStandardItem(_food["nutrition_grades_tags"][0])
                item_code = QStandardItem(_food["code"])
                self._substitutes.appendRow([item_name, item_grade, item_code])

    def populate_product_details(self, code):
        '''Return the full views models of views for show product details'''

        food = openfoodfacts.products.get_by_facets({ "code" : code })
        print("code: ", code, "type:", type(code), "size:", len(food))
        if "product_name_fr" not in food[0]:
            food[0]["product_name_fr"] = food[0]["product_name"]
        self._details["name"] = food[0]["product_name_fr"]
        self._details["description"] = food[0]["ingredients_text"]
        for shop in food[0]["stores_tags"]:
            item = QStandardItem(shop)
            self._details["shops"].appendRow(item)
        self._details["url"] = food[0]["url"]
        self._details["score"] = food[0]["nutrition_grade_fr"]

    @pyqtSlot(QModelIndex)
    def reset_substitute_list(self):
        if self._substitutes:
            self._substitutes.removeRows(0, self._substitutes.rowCount())
            # should reset also product details
            self.reset_product_details()

    @pyqtSlot(QModelIndex)
    def reset_product_details(self):
        if self._details["shops"]:
            self._details["shops"].removeRows(0,
                                self._details["shops"].rowCount())
        self._details["name"] = ""

