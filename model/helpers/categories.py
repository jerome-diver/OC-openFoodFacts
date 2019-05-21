"""Categories model of view helper"""


class CategoriesHelper:

    def __init__(self, database, user):
        self._database = database
        self._user = user

    def records_concerned(self):
        """Tell if category exist in local database table categories"""

        request = "SELECT DISTINCT fc.category_id " \
                  "FROM food_categories AS fc, user_foods AS uf " \
                  "WHERE  fc.food_code = uf.food_code " \
                  "AND uf.user_id = %s ;"
        categories = []
        if self._user:
            value = (self._user.id,)
            for row in self._database.ask_request(request, value):
                categories.append(row["category_id"])
        return categories

    @property
    def user(self):
        """User property access"""

        return self._user

    @user.setter
    def user(self, value):
        """Setter property for user"""

        self._user = value
