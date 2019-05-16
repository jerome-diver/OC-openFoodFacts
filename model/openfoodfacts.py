'''OpenFoodFacts link API of openFoodFacts online with application'''

from model.mainwindow_models import MainWindowModels
from PyQt5.QtCore import pyqtSlot, QModelIndex, Qt
import openfoodfacts
from settings import DEBUG_MODE

class OpenFoodFacts(MainWindowModels):
    '''Model for Open Food Facts data requests'''

    def __init__(self, views=None):
        super().__init__(views)
        self._products_count = 0
        self._checked_substitutes_list = []
        self._checked_details_dict = {}

    @property
    def products_count(self):
        '''Return products count number from last products search'''

        return self._products_count

    @property
    def checked_substitutes_list(self):
        '''Return checked list containing list of codes of substitutes
        validate for be recorded'''

        return self._checked_substitutes_list

    @property
    def checked_details_dict(self):
        '''Return details list as { code: (details) } list from selected
        substitutes products to be recorded'''

        return self._checked_details_dict

    def download_categories(self):
        '''Download categories and return them sorted by name'''

        categories = openfoodfacts.facets.get_categories()
        return sorted(categories, key = lambda kv: kv["name"])

    def download_foods(self, category, page=1):
        '''Return foods from category'''

        def normalize_foods_products(foods_products):
            '''Normalize data products content by adding missing keys'''

            for food in foods_products:
                if "product_name_fr" not in food:
                    food["product_name_fr"] = food["product_name"]

        foods = openfoodfacts.products.advanced_search(
            {   "search_terms" : category,
                "search_tag" : "categories_tags",
                "country" : "france",
                "page": page }
        )
        normalize_foods_products(foods["products"])
        if page == 1:
            self._products_count = foods["count"]
        return sorted(foods["products"],
                      key = lambda kv: kv["product_name_fr"])

    def download_product(self, code, name):
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

        product = openfoodfacts.products.advanced_search( {
                "search_terms" : name,
                "tagtype_0": "codes_tags",
                "tag_contains_0": "contains",
                "tag_0": code,
                "country": "france" })
        if product["count"] == 1:
            normalize(product["products"][0])
            return product["products"][0]
        elif product["count"] == 0 and DEBUG_MODE:
            print("====== NO PRODUCT FOUND ======")
        elif DEBUG_MODE:
            print("====== FIND MANY PRODUCT FOR CODE:", code,
                  "AND [product_name]:", name, "======")
        return None

    def generate_checked_list(self):
        '''Update list of checked item codes'''

        checked_l = []
        for index in range(self._substitutes.rowCount()):
            item = self._substitutes.item(index, 0)
            code = self._substitutes.item(index, 2).text()
            if item.checkState() == Qt.Checked:
                checked_l.append( code )
        self._checked_substitutes_list = checked_l
        if DEBUG_MODE:
            print("checked list:", self._checked_substitutes_list)
