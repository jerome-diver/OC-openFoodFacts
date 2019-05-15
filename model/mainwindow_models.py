'''Models for MainWindow Views:
        categories_list
        foods_list
        substitutes_list
        product_details'''

from PyQt5.QtGui import QStandardItemModel, QStandardItem, \
                        QImage, QPixmap, QColor
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QModelIndex
from settings import NUTRISCORE_A, NUTRISCORE_B, NUTRISCORE_C, \
    NUTRISCORE_D, NUTRISCORE_E, DEBUG_MODE
from urllib.request import urlopen
import re


class MainWindowModels(QObject):
    '''MainWindow Models'''

    def __init__(self, views=None):
        super().__init__()
        self._views = views
        if views != None:
            self._db_categories = []
            self._categories = QStandardItemModel(self._views['categories'])
            self._foods = QStandardItemModel(self._views["foods"])
            self._substitutes = QStandardItemModel(self._views["substitutes"])
            self._substitutes.setHorizontalHeaderLabels(["Nom", "Grade", "Code"])
            self._details = { "name": "",
                              "description" : "",
                              "shops" : QStandardItemModel(self._views["shops"]),
                              "url" : "",
                              "score" : "",
                              "score_data": "",
                              "brand" : "",
                              "packaging" : "",
                              "img_thumb" : "",
                              "img_data": None,
                              "code" : "",
                              }
            self._codes = []
            self._foods_recorded = [] # [ [] ]  |as pages of foods
            self._selected_categroy = None
            self._selected_food = ()
            self._selected_substitutes = []

    @property
    def categories(self):
        '''categories list model'''

        return self._categories

    @property
    def foods(self):
        '''Foods list model'''

        return self._foods

    @property
    def substitutes(self):
        '''Substitutes list model'''

        return self._substitutes

    @property
    def details(self):
        '''Details of selected product models'''

        return self._details

    @property
    def selected_substitutes(self):
        '''Selected substitutes list (checked from substitutes list view)'''

        return self._selected_substitutes

    @selected_substitutes.setter
    def selected_substitutes(self, value):
        '''Set self._selected_substitutes'''

        self._selected_substitutes = value

    @property
    def selected_food(self):
        '''Selected food (from food list view)'''

        return self._selected_food

    def populate_categories(self, categories):
        '''Return all categories inside list categories view
        by openfoodfacts module helper'''

        self._categories.removeRows(0, self._foods.rowCount())
        self._foods_recorded = []
        for category in categories:
            is_fr = re.match(r'^fr:', category["name"])
            is_latin_chars = re.match(r'[0-9a-zA-z\s]', category["name"])
            if is_latin_chars:
                find = re.sub(r'^fr:', '', category["name"]) if is_fr \
                    else category["name"]
                item_name = QStandardItem(find)
                item_id = QStandardItem(category["id"])
                self._categories.appendRow([item_name, item_id])

    def populate_foods(self, foods, new=True):
        '''Return the list wiew of foods for give category string
        with openfoodfacts library helper'''

        if new:
            self._foods.removeRows(0, self._foods.rowCount())
        for food in foods:
            key = "product_name_fr"
            if food[key].strip().isspace() or food[key] == '' and DEBUG_MODE:
                print("no way (no product name) for:", food["codes_tags"][1])
            else:
                item = QStandardItem(food[key].strip())
                code = QStandardItem(food["codes_tags"][1])
                score = QStandardItem(food["nutrition_grades_tags"][0])
                self._foods.appendRow([item, code, score])
            self._codes.append(food["codes_tags"][1])
        self._foods.sort(0)


    def populate_substitutes(self, food, page=0, new=True):
        '''Return the list of possible substitution products inside
        substitutes list view'''

        if new:
            self._substitutes.removeRows(0, self._substitutes.rowCount())
        for _food in self._foods_recorded[page]:
            if _food["product_name_fr"] != food \
                    and _food["nutrition_grades_tags"][0] != "not-applicable" \
                    and _food["codes_tags"][1] not in self._empty_product_code\
                    and _food["nutrition_grades_tags"][0] <= \
                        self._selected_food[1] :
                item_name = QStandardItem(_food["product_name_fr"])
                item_name.setCheckable(True)
                item_grade = QStandardItem(_food["nutrition_grades_tags"][0])
                item_code = QStandardItem(_food["codes_tags"][1])
                if "brands_tags" not in _food.keys():
                    if DEBUG_MODE:
                        print("missing brands_tags for:", _food["codes_tags"][1])
                    item_name.setBackground(QColor(255,102,0))
                    item_code.setBackground(QColor(255,102,0))
                self._substitutes.appendRow([item_name, item_grade, item_code])
        self._substitutes.sort(1)

    def populate_product_details(self, food):
        '''Return the full views models of views for show product details'''

        url = "<a href=\"" + food["url"] + "\" />"
        self._details["code"] = food["codes_tags"][1]
        self._details["shops"].removeRows(0, self._details["shops"].rowCount())
        self._details["name"] = url + food["product_name_fr"] + "</a>"
        self._details["description"] = food["ingredients_text"]
        for shop in food["stores_tags"]:
            item = QStandardItem(shop)
            self._details["shops"].appendRow(item)
        self._details["url"] = food["url"]
        score = food["nutrition_grades_tags"][0]
        self._details["score_data"] = score
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
        self._details["score"].scaledToWidth(64)
        self._details["packaging"] = food["packaging"]
        self._details["brand"] = food["brands_tags"]
        img_url = food["image_front_url"]
        data_front = urlopen(img_url).read()
        self._details["img_data"] = data_front
        img_front = QImage()
        img_front.loadFromData(data_front)
        self._details["img_thumb"] = QPixmap(img_front)
        self._details["img_thumb"].scaledToWidth(150)

    def reset_foods_list(self):
        '''Reset the foods list'''

        self._selected_food = ()
        self._foods.removeRows(0, self._foods.rowCount())

    def reset_substitutes_list(self):
        '''Reset model for substitutes_list view'''

        self._selected_substitutes = []
        self._substitutes.removeRows(0, self._substitutes.rowCount())

    def reset_product_details(self):
        '''Reset models for product details views'''

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

