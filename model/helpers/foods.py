"""Foods model of view helper"""
from settings import DEBUG_MODE


class FoodsHelper:

    def __init__(self, user):
        self._user = user
        self._connection = user.connection

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
    def user(self):
        """User property access"""

        return self._user

    @user.setter
    def user(self, usr):
        """Setter property for user"""

        self._user = usr
        self._connection = usr.connection

    @property
    def connection(self):
        """Property for self connection"""

        return self._connection

    @connection.setter
    def connection(self, db):
        """Setter property for connection"""

        self._connection = db