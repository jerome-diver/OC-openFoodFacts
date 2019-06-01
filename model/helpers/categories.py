"""Categories model of view helper"""

from model.helpers import MixinHelpers


class CategoriesHelper(MixinHelpers):
    """Helper for Categories"""

    def __init__(self, user):
        super().__init__(user)

    def records_concerned(self):
        """Tell if category exist in local connection table categories"""

        request = "SELECT DISTINCT fc.category_id " \
                  "FROM food_categories AS fc, user_foods AS uf " \
                  "WHERE  fc.food_code = uf.food_code " \
                  "AND uf.user_id = %s ;"
        categories = []
        if self._user:
            value = (self._user.id,)
            for row in self._connection.ask_request(request, value):
                categories.append(row["category_id"])
        return categories

