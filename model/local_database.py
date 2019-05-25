"""Local Database mode model"""

from PyQt5.QtCore import QObject, pyqtSlot

from settings import DEBUG_MODE
from model import User
from . import CategoriesModel, FoodsModel, \
              SubstitutesModel, ProductDetailsModels
from . import CategoriesHelper, FoodsHelper, SubstitutesHelper
from controller import Widget


class LocalDatabaseModel(QObject):
    """Local Database model Object"""

    def __init__(self, views, authenticate):
        super().__init__()
        self._views = views
        self._authenticate = authenticate
        self._user = authenticate.user
        self._connection = self._user.connection
        self._categories = CategoriesModel(views, CategoriesHelper(
            self._connection, self._user))
        self._foods = FoodsModel(views, FoodsHelper(
            self._connection, self._user))
        self._substitutes = SubstitutesModel(
            views, SubstitutesHelper(self._connection, self._user))
        self._product_details = ProductDetailsModels(views)

    @property
    def categories(self):
        """Categories property"""

        return self._categories

    @property
    def foods(self):
        """Foods property"""

        return self._foods

    @property
    def substitutes(self):
        """Substitutes property"""

        return self._substitutes

    @property
    def product_details(self):
        """Product details property"""

        return self._product_details

    def get_categories(self):
        """Get categories from local  database"""

        categories = []
        request = "SELECT * FROM categories;"
        for row in self._connection.ask_request(request):
            categories.append({"id": row["id"], "name": row["name"]})
        return categories

    def get_foods(self, category):
        """Get foods for current category"""

        foods = []
        request = """
            SELECT f.name, f.code, f.score 
                FROM foods AS f, food_categories AS fc 
                WHERE fc.food_code = f.code 
                AND fc.category_id = %s ;"""
        values = (category, )
        for row in self._connection.ask_request(request, values):
            food = {"product_name_fr": row["name"],
                    "code": row["code"],
                    "nutrition_grades_tags": [row["score"]]}
            foods.append(food)
        if DEBUG_MODE:
            print("search foods for category:", category)
            print("found:", foods)
        return foods

    def get_substitutes(self, code):
        """Get product details from code and name"""

        substitutes = [[]]
        request = """
            SELECT f.brand, f.name, f.score, f.code 
                FROM foods AS f, food_substitutes AS fs 
                WHERE f.code = fs.substitute_code 
                AND fs.food_code = %s ;"""
        values = (code, )
        for row in self._connection.ask_request(request, values):
            substitute = {
                "product_name_fr": row["name"],
                "nutrition_grades_tags": [row["score"]],
                "code": row["code"],
                "brands_tags": row["brand"],
                "stores_tags": []}
            req = """
                SELECT DISTINCT shop_name 
                    FROM food_shops  
                    WHERE food_code = %s ;"""
            val = (row["code"], )
            for r in self._connection.ask_request(req, val):
                substitute["stores_tags"].append(r["shop_name"])
            substitutes[0].append(substitute)
        return substitutes


    def get_product_details(self, code):
        """Get product details from code and name"""

        request = """
            SELECT * FROM foods WHERE code = %s ;"""
        values = (code,)
        for row in self._connection.ask_request(request, values):
            product_details = {
                "code": row["code"],
                "product_name_fr": row["name"],
                "ingredients_text": row["description"],
                "nutrition_grades_tags": [row["score"]],
                "url": row["url"],
                "packaging": row["packaging"],
                "brands_tags": row["brand"],
                "image_front_url": row["image_url"],
                "stores_tags": []}
            req = """
                SELECT DISTINCT shop_name 
                    FROM food_shops 
                    WHERE food_code = %s ;"""
            val = (row["code"], )
            for r in self._connection.ask_request(req, val):
                product_details["stores_tags"].append(r["shop_name"])
            return product_details

    @pyqtSlot(User)
    def on_user_connected(self, user):
        """When a user is connected"""

        self._user = user

    def reset_models(self, models=(Widget.ALL,)):
        """Reset all models or elected ones"""

        if Widget.CATEGORIES in models or Widget.ALL in models:
            self._categories.reset()
        if Widget.FOODS in models or Widget.ALL in models:
            self._foods.reset()
        if Widget.SUBSTITUTES in models or Widget.ALL in models:
            self._substitutes.reset()
        if Widget.DETAILS in models or Widget.ALL in models:
            self._product_details.reset()
