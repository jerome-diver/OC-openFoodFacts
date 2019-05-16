'''Models for product details views of Mainwindow'''

from urllib.request import urlopen
from PyQt5.QtGui import QStandardItemModel, QStandardItem, \
                        QImage, QPixmap

from settings import NUTRISCORE_A, NUTRISCORE_B, NUTRISCORE_C, \
    NUTRISCORE_D, NUTRISCORE_E

class ProductDetailsModels():
    '''Mainwindow product details views models'''

    def __init__(self, views):
        super().__init__()
        self._views = views
        self._details = {"name": "",
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

    @property
    def details(self):
        '''Details of selected product models'''

        return self._details

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
        if score == "a": self._details["score"] = QPixmap(NUTRISCORE_A)
        if score == "b": self._details["score"] = QPixmap(NUTRISCORE_B)
        if score == "c": self._details["score"] = QPixmap(NUTRISCORE_C)
        if score == "d": self._details["score"] = QPixmap(NUTRISCORE_D)
        if score == "e": self._details["score"] = QPixmap(NUTRISCORE_E)
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

    def reset_product_details(self):
        '''Reset models for product details views'''

        if self._details["shops"]:
            self._details["shops"].removeRows(0,
                                              self._details["shops"].
                                              rowCount())
        self._details["name"] = ""
        self._details["description"] = ""
        self._details["url"] = ""
        self._details["score"] = QPixmap()
        self._details["brand"] = ""
        self._details["packaging"] = ""
        self._details["img_thumb"] = QPixmap()
