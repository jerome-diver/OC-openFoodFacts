"""Foods model of view helper"""


class FoodsHelper:

    def __init__(self, database, user):
        self._database = database
        self._user = user

    def records_concerned(self, category_id):
        """Tell if category exist in local database table categories"""

        request = "SELECT DISTINCT f.code  " \
                  "FROM food_categories AS fc, foods AS f, user_foods AS uf" \
                  "WHERE  fc.category_id = %s" \
                  "AND fc.food_code = f.code" \
                  "AND uf.user_id = %s " \
                  "AND uf.food_code = f.code ;"
        foods = []
        if self._user:
            values = (category_id, self._user.id)
            for row in self._database.ask_request(request, values):
                foods.append(row["id"])
        return foods
