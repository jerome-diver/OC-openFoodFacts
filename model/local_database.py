"""Local Database mode model"""

from settings import DEBUG_MODE
from . import MixinModels


class LocalDatabase(MixinModels):
    """Local Database model Object"""

    def __init__(self, **kargs):
        super().__init__(**kargs)

    def get_categories(self):
        """Get categories from local  database"""

        categories = []
        request = "SELECT DISTINCT c.* " \
                  "FROM categories AS c, " \
                  "     food_categories AS fc," \
                  "     user_foods AS uf " \
                  "WHERE uf.user_id = %s " \
                  "AND uf.food_code = fc.food_code " \
                  "AND fc.category_id = c.id;"
        values = (self._user.id,)
        for row in self._connection.ask_request(request, values):
            categories.append({"id": row["id"], "name": row["name"]})
        return categories

    def get_foods(self, category):
        """Get foods for current category"""

        foods = []
        request = """
            SELECT f.name, f.code, f.score 
                FROM foods AS f, 
                     food_categories AS fc,
                     user_foods AS uf 
                WHERE fc.food_code = f.code
                AND uf.food_code = f.code 
                AND fc.category_id = %s
                AND uf.user_id = %s ;"""
        values = (category, self._user.id)
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


