"""Models for product details views of Mainwindow"""

from urllib.request import urlopen
from PyQt5.QtGui import QStandardItemModel, QStandardItem, \
                        QImage, QPixmap

from settings import NUTRISCORE_A, NUTRISCORE_B, NUTRISCORE_C, \
    NUTRISCORE_D, NUTRISCORE_E, DEBUG_MODE


class ProductDetailsModels():
    """MainWindow product details views models"""

    def __init__(self, views):
        self._views = views
        self._models = {"name": "",
                        "description": "",
                        "shops": QStandardItemModel(self._views["shops"]),
                        "shops_names": [],
                        "url": "",
                        "score": "",
                        "score_data": "",
                        "brand": "",
                        "packaging": "",
                        "img_thumb": "",
                        "img_data": None,
                        "code": "",
                        }
        self._checked = {}

    def populate(self, food):
        """Return the full views models of views for show product details"""

        url = "<a href=\"" + food["url"] + "\" />"
        self._models["code"] = food["code"]
        self._models["shops"].removeRows(0, self._models["shops"].rowCount())
        self._models["name"] = url + food["product_name_fr"] + "</a>"
        self._models["description"] = food["ingredients_text"]
        for shop in food["stores_tags"]:
            self._models["shops_names"].append(shop)
            item = QStandardItem(shop)
            self._models["shops"].appendRow(item)
        self._models["url"] = food["url"]
        score = food["nutrition_grades_tags"][0]
        self._models["score_data"] = score
        if score == "a": self._models["score"] = QPixmap(NUTRISCORE_A)
        if score == "b": self._models["score"] = QPixmap(NUTRISCORE_B)
        if score == "c": self._models["score"] = QPixmap(NUTRISCORE_C)
        if score == "d": self._models["score"] = QPixmap(NUTRISCORE_D)
        if score == "e": self._models["score"] = QPixmap(NUTRISCORE_E)
        self._models["score"].scaledToWidth(64)
        self._models["packaging"] = food["packaging"]
        self._models["brand"] = food["brands_tags"]
        img_url = food["image_front_url"] \
            if "image_front_url" in food.keys() else ""
        if img_url:
            data_front = urlopen(img_url).read()
            self._models["img_data"] = data_front
            img_front = QImage()
            img_front.loadFromData(data_front)
            self._models["img_thumb"] = QPixmap(img_front)
            self._models["img_thumb"].scaledToWidth(150)
        if DEBUG_MODE:
            print("=============================================")
            if "code" in food.keys():
                print("code:", food["code"])
            if "codes_tags" in food.keys():
                print("codes_tags:", food["codes_tags"])
            if "id" in food.keys():
                print("id:", food["id"])
            if "_id" in food.keys():
                print("_id:", food["_id"])
            if "id_" in food.keys():
                print("_id:", food["id_"])
            print("=============================================")

    @staticmethod
    def define_with(var, food):
        """define variables records datas"""

        var["code"] = food["code"] if "code" in food \
                      else food["codes_tags"][1]
        var["name"] = food["product_name_fr"]
        var["description"] = food["ingredients_text"]
        var["shops_names"] = []
        for shop in food["stores_tags"]:
            var["shops_names"].append(shop)
        var["url"] = food["url"]
        var["score_data"] = food["nutrition_grades_tags"][0]
        var["packaging"] = food["packaging"]
        var["brand"] = food["brands_tags"]
        img_url = food["image_front_url"] \
            if "image_front_url" in food.keys() else ""
        # case of blob field format for data insertion in database:
        #data_front = urlopen(img_url).read()
        #var["image"] = data_front
        var["img_url"] = img_url
        
    def reset(self):
        """Reset models for product details views"""

        if self._models["shops"]:
            self._models["shops"].removeRows(0,
                                              self._models["shops"].
                                              rowCount())
        self._models["name"] = ""
        self._models["description"] = ""
        self._models["url"] = ""
        self._models["score"] = QPixmap()
        self._models["brand"] = ""
        self._models["packaging"] = ""
        self._models["img_thumb"] = QPixmap()
        self._checked = {}
        print("======== RESET ProductDetailsModels ======")

    def update_checked(self, details, add=True):
        """Update checked dictionary with nex code"""

        data = {}
        self.define_with(data, details)
        if add:
            self._checked[data["code"]] = (
                data["name"],
                data["description"],
                data["score_data"],
                data["brand"],
                data["packaging"],
                data["url"],
                data["img_url"],
                data["shops_names"])
        else:
            if data["code"] in self._checked:
                del self._checked[data["code"]]
        if DEBUG_MODE:
            print("=======  P r o d u c t D e t a i l s M o d e l s  =======")
            print("details keys list:", self._checked.keys())
            print("detals list:", self._checked)

    @property
    def models(self):
        """Details of selected product models"""

        return self._models

    @property
    def checked(self):
        """Checked list of substitutes products property"""

        return self._checked

