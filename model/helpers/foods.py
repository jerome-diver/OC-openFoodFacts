"""Foods model of view helper"""
from settings import DEBUG_MODE


class FoodsHelper:

    def __init__(self, database, user):
        self._database = database
        self._user = user

    def records_concerned(self, category_id):
        """Tell if category exist in local database table categories"""

        request = "SELECT DISTINCT fc.food_code  "\
                  "FROM food_categories AS fc,  user_foods AS uf "\
                  "WHERE fc.food_code = uf.food_code "\
                  "AND fc.category_id = %s "\
                  "AND uf.user_id = %s ;"
        foods = []
        if self._user:
            if DEBUG_MODE:
                print("== HELPER == is searching for foods of category id:",
                      category_id," in local database for user:",
                      self._user.id)
            values = (category_id, self._user.id)
            for row in self._database.ask_request(request, values):
                foods.append(row["food_code"])
        return foods

    @property
    def user(self):
        """User property access"""

        return self._user

    @user.setter
    def user(self, value):
        """Setter property for user"""

        self._user = value
