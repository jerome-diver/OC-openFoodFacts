'''Local Database mode model'''


from PyQt5.QtCore import QObject, Qt, pyqtSignal

from settings import DEBUG_MODE
from . import CategoriesModel
from . import FoodsModel
from . import SubstitutesModel
from . import ProductDetailsModels

class LocalDatabaseModel(QObject):
    '''Local Database model Object'''

    def __init__(self, views, database):
        super().__init__()
        self._views = views
        self._database = database
        self._categories = CategoriesModel(views)
        self._foods = FoodsModel(views)
        self._substitutes = SubstitutesModel(views)
        self._product_details = ProductDetailsModels(views)

    @property
    def categories(self):
        '''Categories property'''

        return self._categories

    @property
    def foods(self):
        '''Foods property'''

        return self._foods

    @property
    def substitutes(self):
        '''Substitutes property'''

        return self._substitutes

    @property
    def product_details(self):
        '''Product details property'''

        return self._product_details

    def get_categories(self):
        '''Get categories from local  database'''

        categories = []
        request = "SELECT * FROM categories;"
        for row in self._database.ask_request(request):
            categories.append({ "id": row["id"], "name": row["name"]})
        return categories

    def get_foods(self, category):
        '''Get foods for current categrory'''

        foods = []
        request = "SELECT f.name_, f.code, f.score " \
                  "FROM foods AS f, food_categories AS fc " \
                  "WHERE fc.food_code = f.code " \
                  "AND fc.category_id = %s ;"
        values = (category, )
        for row in self._database.ask_request(request, values):
            food = {}
            food["product_name_fr"] = row["name_"]
            food["codes_tags"] = [None, row["code"]]
            food["nutrition_grades_tags"] = [row["score"]]
            foods.append(food)
        return foods

    def get_substitutes(self, code, name):
        '''Get product details from code and name'''

        substitutes = []
        request = "SELECT f.brand, f.store, f.name_, f.score, f.code " \
                  "FROM foods AS f, food_substitutes AS fs" \
                  "WHERE fs.food_code = f.code " \
                  "AND fs.substitute_code = %s " \
                  "AND f.name_ = %s ;"
        values = (code, name)
        for row in self._database.ask_request(request, values):
            substitute = {}
            substitute["product_name_fr"] = row["name_"]
            substitute["nutrition_grades_tags"] = [row["score"]]
            substitute["codes_tags"] = [None, row["code"]]
            if row["brand"] != '':
                substitute["brands_tags"] = row["brand"]
            req = "SELECT food_shops.shop_id FROM food_shop, foods " \
                  "WHERE foods.code = %s ;"
            val = (row["code"], )
            answer = ""
            for r in self._database.ask_request(req, val):
                answer = r["shop_id"]
            if answer != "":
                substitute["stores_tags"] = [answer]
            substitutes.append(substitute)
        return substitutes


    def get_substitute_details(self, code, name):
        '''Get product details from code and name'''

        product_details = {}
        request = "SELECT f.* FROM foods AS f, food_substitutes AS fs " \
                  "WHERE f.code = fs.food_code " \
                  "AND fs.substitute_code = %s" \
                  "AND f.name_ = %s ;"
        values = (code, name)
        for row in self._database.ask_request(request, values):
            product_details["codes_tags"] = [None, row["code"]]
            product_details["product_name_fr"] = row["name_"]
            product_details["ingredients_text"] = row["description"]
            product_details["nutrition_grades_tags"] = [row["score"]]
            product_details["url"] = row["url"]
            product_details["packaging"] = row["packaging"]
            product_details["brands_tags"] = row["brand"]
            product_details["image_front_url"] = row["image_url"]
            req = "SELECT s.name " \
                  "FROM food_shop AS fs, shops AS s " \
                  "WHERE fs.food_code = %s AND s.id = fs.shop_id;"
            val = (row["code"], )
            product_details["stores_tags"] = []
            for r in self._database.ask_request(req, val):
                product_details["stores_tags"].append(r["name"])
            return product_details
