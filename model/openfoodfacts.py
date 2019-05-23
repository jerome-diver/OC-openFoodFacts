"""OpenFoodFacts link API of openFoodFacts online with application"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import openfoodfacts

from settings import DEBUG_MODE
from model import User
from . import CategoriesModel, FoodsModel, \
              SubstitutesModel, ProductDetailsModels
from . import CategoriesHelper, FoodsHelper, SubstitutesHelper
from controller import Widget


class OpenFoodFacts(QObject):
    """Model for Open Food Facts data requests"""

    internet_access = pyqtSignal(bool)

    def __init__(self, views=None, database=None):
        super().__init__()
        self._user = None
        if views and database:
            self._categories = CategoriesModel(views,
                                               CategoriesHelper(database,
                                                                self._user))
            self._foods = FoodsModel(views,
                                     FoodsHelper(database, self._user))
            self._substitutes = SubstitutesModel(views,
                                                 SubstitutesHelper(database,
                                                                   self._user))
            self._product_details = ProductDetailsModels(views)
        else:
            self._substitutes = None
            self._foods = None
            self._categories = None
            self._product_details = None

    def download_categories(self):
        """Download categories and return them sorted by name"""

        categories = None
        try:
            categories = openfoodfacts.facets.get_categories()
        except:
            self.internet_access.emit(False)
            return categories
        self.internet_access.emit(True)
        categories = [c for c in categories if c["products"] >= 2]
        return sorted(categories, key=lambda kv: kv["name"])

    def download_foods(self, category, page=1):
        """Return foods from category"""

        def normalize_foods_products(foods_products):
            """Normalize data products content by adding missing keys"""

            for food in foods_products:
                wrong = False
                if "code" not in food.keys():
                    if "id" not in food.keys():
                        wrong = True
                    else:
                        food["code"] = food["id"]
                if "product_name_fr" not in food:
                    if "product_name" in food:
                        if food["product_name"].isspace():
                            wrong = True
                        elif food["product_name"] == '':
                            wrong = True
                        else:
                            food["product_name_fr"] = food["product_name"]
                    else:
                        wrong = True
                elif food["product_name_fr"].isspace():
                    wrong = True
                elif food["product_name_fr"] == "":
                    wrong = True
                if wrong:
                    foods_products.remove(food)

        foods = None
        try:
            foods = openfoodfacts.products.get_by_category(category, page=page)
        except:
            self.internet_access.emit(False)
            return foods
        self.internet_access.emit(True)
        normalize_foods_products(foods)
        #return sorted(foods, key=lambda kv: kv["product_name_fr"])
        return foods

    def download_product(self, code, name):
        """Return product for this code"""

        def normalize(product):
            """Normalize API keys"""

            if "product_name_fr" not in product:
                if "product_name" in product:
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

        product = None
        try:
            product = openfoodfacts.products.advanced_search({
                "search_terms": name,
                "tagtype_0": "code",
                "tag_contains_0": "contains",
                "tag_0": code,
                "country": "france"})
        except:
            self.internet_access.emit(False)
            return product
        self.internet_access.emit(True)
        if product["count"] == 1:
            normalize(product["products"][0])
            return product["products"][0]
        if product["count"] == 0 and DEBUG_MODE:
            print("====== NO PRODUCT FOUND ======")
        elif DEBUG_MODE:
            print("====== FIND MANY PRODUCT FOR CODE:", code,
                  "AND [product_name]:", name, "======")
        return None

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

    @pyqtSlot(User)
    def on_user_connected(self, user):
        """When a user is connected"""

        self._user = user
        self.categories.helper.user = user
        self.foods.helper.user = user
        self.substitutes.helper.user = user
        if self.categories.rowCount():
            self.categories.find_categories_in_database()
        if self.foods.rowCount():
            self.foods.find_foods_in_database()
        if self.substitutes.rowCount():
            self.substitutes.find_substitutes_in_database(
                self.foods.selected[0])
        if DEBUG_MODE:
            print("get user", self._user.username, "connected")

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

