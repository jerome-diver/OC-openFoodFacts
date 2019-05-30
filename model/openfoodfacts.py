"""OpenFoodFacts link API of openFoodFacts online with application"""

import openfoodfacts

from settings import DEBUG_MODE
from . import MixinModels


class OpenFoodFacts(MixinModels):
    """Model for Open Food Facts data requests"""

    def __init__(self, **kargs):
        super().__init__(**kargs)

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
        else:
            self.internet_access.emit(True)
            normalize_foods_products(foods)
        finally:
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
            print("======  O p e n F o o d F a c t s  (model)  =====")
            print("====== NO PRODUCT FOUND ======")
        elif DEBUG_MODE:
            print("======  O p e n F o o d F a c t s  (model)  =====")
            print("Find products for code:", code,
                  "and [product_name]:", name)
        return None
