"""OpenFoodFacts link API of openFoodFacts online with application"""

from PyQt5.QtCore import QObject, Qt, pyqtSignal
import openfoodfacts

from settings import DEBUG_MODE
from . import CategoriesModel
from . import FoodsModel
from . import SubstitutesModel
from . import ProductDetailsModels
from controller import Widget


class OpenFoodFacts(QObject):
    """Model for Open Food Facts data requests"""

    internet_access = pyqtSignal(bool)

    def __init__(self, views=None):
        super().__init__()
        if views:
            self._categories = CategoriesModel(views)
            self._foods = FoodsModel(views)
            self._substitutes = SubstitutesModel(views)
            self._product_details = ProductDetailsModels(views)
        else:
            self._substitutes = None
            self._foods = None
            self._categories = None
            self._product_details = None

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
                if "product_name_fr" not in food:
                    if "product_name" in food:
                        food["product_name_fr"] = food["product_name"]
                    else:
                        foods_products.remove(food)

        foods = None
        try:
            foods = openfoodfacts.products.get_by_category(category, page=page)
        except:
            self.internet_access.emit(False)
            return foods
        self.internet_access.emit(True)
        normalize_foods_products(foods)
        return sorted(foods, key=lambda kv: kv["product_name_fr"])

    def download_product(self, code, name):
        """Return product for this code"""

        def normalize(product):
            """Normalize API keys"""

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

        product = None
        try:
            product = openfoodfacts.products.advanced_search({
                "search_terms": name,
                "tagtype_0": "codes_tags",
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
