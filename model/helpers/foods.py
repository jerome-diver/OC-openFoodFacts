"""Foods model of view helper"""
from settings import DEBUG_MODE
from . import MixinHelpers


class FoodsHelper(MixinHelpers):
    """Helper for Foods"""

    def __init__(self, user):
        super().__init__(user)

    def records_concerned(self, category_id):
        """Tell if category exist in local connection table categories"""

        request = "SELECT DISTINCT fc.food_code  "\
                  "FROM food_categories AS fc, " \
                  "     user_foods AS uf "\
                  "WHERE fc.food_code = uf.food_code "\
                  "AND fc.category_id = %s "\
                  "AND uf.user_id = %s " \
                  "ANd fc.food_code IN (" \
                  "     SELECT DISTINCT food_code " \
                  "     FROM food_substitutes " \
                  "     WHERE user_id = %s) ;"

        foods = []
        if self._user:
            if DEBUG_MODE:
                print("=====  F o o d s H e l p e r  =====")
                print("is searching for foods of category id:",
                      category_id)
                print("in local connection for user:",
                      self._user.id)
                print("where have any substitute")
            values = (category_id, self._user.id, self._user.id)
            for row in self._connection.ask_request(request, values):
                foods.append(row["food_code"])
        return foods

    @property
    def connection(self):
        """Property for self connection"""

        return self._connection

    @connection.setter
    def connection(self, db):
        """Setter property for connection"""

        self._connection = db