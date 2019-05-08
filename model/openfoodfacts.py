'''OpenFoodFacts link API of openFoodFacts online with application'''

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QImage, QPixmap
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QModelIndex
from settings import NUTRISCORE_A, NUTRISCORE_B, NUTRISCORE_C, \
                     NUTRISCORE_D, NUTRISCORE_E
import openfoodfacts
import requests
from urllib.request import urlopen
import re

class OpenFoodFacts(QObject):
    '''Model for Open Food Facts data requests'''

    error_signal = pyqtSignal(str)
    status_message = pyqtSignal(str)
    update_details_view = pyqtSignal()

    def __init__(self, database, views):
        super().__init__()
        self._database = database
        self._views = views
        self._db_categories = []
        self._categories = QStandardItemModel(self._views['categories'])
        self._foods = QStandardItemModel(self._views["foods"])
        self._foods_recorded = []
        self._substitutes = QStandardItemModel(self._views["substitutes"])
        self._substitutes.setHorizontalHeaderLabels(["Nom", "Grade", "Code"])
        self._details = { "name": "",
                          "description" : "",
                          "shops" : QStandardItemModel(self._views["shops"]),
                          "url" : "",
                          "score" : "",
                          "brand" : "",
                          "packaging" : "",
                          "img_thumb" : "",
                          }
        self._codes = []
        self._empty_product_code = []

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

    def download_categories(self):
        '''Download categories and return them sorted by name'''

        req = requests.get("https://fr.openfoodfacts.org/categories.json")
        categories = req.json()["tags"]
        #categories = openfoodfacts.facets.get_categories()
        return sorted(categories, key = lambda kv: kv["name"])


    def populate_categories(self, categories):
        '''Return all categories inside list categories view
        by openfoodfacts module helper'''

        self._categories.removeRows(0, self.foods.rowCount())
        for category in categories:
            is_fr = re.match(r'^fr:', category["name"])
            is_latin_chars = re.match(r'[0-9a-zA-z\s]', category["name"])
            if is_latin_chars:
                find = re.sub(r'^fr:', '', category["name"]) if is_fr \
                    else category["name"]
                item_name = QStandardItem(find)
                item_id = QStandardItem(category["id"])
                self._categories.appendRow([item_name, item_id])

    def populate_foods(self, category):
        '''Return the list wiew of foods for give category string
        with openfoodfacts library helper'''

        def get_food_item(this, food, key):
            '''Define item'''

            if food[key].strip().isspace() or food[key] == '':
                print("no way for:", food[key])
            else:
                item = QStandardItem(food[key].strip())
                code = QStandardItem(food["code"])
                this._foods.appendRow([item, code])
            return food["code"]

        def normalize_foods_products(foods_products):
            '''Normalize data products content by adding missing keys'''

            for food in foods_products:
                if "product_name_fr" not in food:
                    food["product_name_fr"] = food["product_name"]

        self.foods.removeRows(0, self.foods.rowCount())
        foods = openfoodfacts.products.advanced_search(
            {   "search_terms" : category,
                "search_tag" : "categories_tags",
                "country" : "france" }
        )
        normalize_foods_products(foods["products"])
        sorted_foods = sorted(foods["products"],
                              key = lambda kv: kv["product_name_fr"])
        self._foods_recorded = sorted_foods
        for food in sorted_foods:
            self._codes.append(get_food_item(self, food, "product_name_fr"))


    def populate_substitutes(self, food):
        '''Return the list of possible substitution products inside
        substitutes list view'''

        self.substitutes.removeRows(0, self.substitutes.rowCount())
        foods_grade_sorted = sorted(self._foods_recorded,
                                    key = lambda kv:
                                    kv["nutrition_grades_tags"][0])
        for _food in foods_grade_sorted:
            if _food["product_name_fr"] != food \
                    and _food["nutrition_grades_tags"][0] != "not-applicable"\
                    and _food["code"] not in self._empty_product_code:
                item_name = QStandardItem(_food["product_name_fr"])
                item_name.setCheckable(True)
                item_grade = QStandardItem(_food["nutrition_grades_tags"][0])
                item_code = QStandardItem(_food["code"])
                self._substitutes.appendRow([item_name, item_grade, item_code])

    def get_product(self, code):
        '''Return product for this code'''

        def normalize(product):
            '''Normalize API keys'''

            if "product_name_fr" not in product:
                product["product_name_fr"] = product["product_name"]
            if "nutrition_grade_fr" not in product:
                if "nutrition_grade" in product:
                    product["nutrition_grade_fr"] = product["nutrition_grade"]
                else:
                    product["nutrition_grade_fr"] = "e"
            if "ingredients_text" not in product:
                product["ingredients_text"] = "--aucune description--"
            if "packaging" not in product:
                product["packaging"] = "--aucune indication--"
            if "brands_tags" not in product:
                product["brands_tags"] = ""
            if isinstance(product["brands_tags"], list):
                brands = ""
                for brand in product["brands_tags"]:
                    brands += ", " + brand if brands != "" else brand
                product["brands_tags"] = brands
            if "stores_tags" not in product:
                product["stores_tags"] = ""

        product = openfoodfacts.products.get_by_facets({ "code" : code })
        if product and len(product[0]) != 0:
            normalize(product[0])
            return product[0]
        return None

    def populate_product_details(self, code):
        '''Return the full views models of views for show product details'''

        food = self.get_product(code)
        if food:
            url = "<a href=\"" + food["url"] + "\" />"
            self._details["shops"].removeRows(0,
                                    self._details["shops"].rowCount())
            self._details["name"] = url + food["product_name_fr"] + "</a>"
            self._details["description"] = food["ingredients_text"]
            for shop in food["stores_tags"]:
                item = QStandardItem(shop)
                self._details["shops"].appendRow(item)
            self._details["url"] = food["url"]
            score = food["nutrition_grade_fr"]
            if score == "a":
                self._details["score"] = QPixmap(NUTRISCORE_A)
            if score == "b":
                self._details["score"] = QPixmap(NUTRISCORE_B)
            if score == "c":
                self._details["score"] = QPixmap(NUTRISCORE_C)
            if score == "d":
                self._details["score"] = QPixmap(NUTRISCORE_D)
            if score == "e":
                self._details["score"] = QPixmap(NUTRISCORE_E)
            self._details["score"].scaled(32, 64)
            self._details["packaging"] = food["packaging"]
            self._details["brand"] = food["brands_tags"]
            img_url = food["image_front_url"]
            data_front = urlopen(img_url).read()
            img_front = QImage()
            img_front.loadFromData(data_front)
            self._details["img_thumb"] = QPixmap(img_front)
        else:
            self.reset_product_details()
            self.error_signal.emit("Hélas, il n'y a aucun détail enregistré "
                                   "pour ce code produit")
            self.status_message.emit("Aucun détail cohérent n'est fourni")

    @pyqtSlot(QModelIndex)
    def reset_substitute_list(self):
        if self._substitutes:
            self._substitutes.removeRows(0, self._substitutes.rowCount())
            self.reset_product_details()

    @pyqtSlot(QModelIndex)
    def reset_product_details(self):
        if self._details["shops"]:
            self._details["shops"].removeRows(0,
                                self._details["shops"].rowCount())
        self._details["name"] = ""
        self._details["description"] =""
        self._details["url"] =  ""
        self._details["score"] = QPixmap()
        self._details["brand"] = ""
        self._details["packaging"] = ""
        self._details["img_thumb"] = QPixmap()
        self.update_details_view.emit()
