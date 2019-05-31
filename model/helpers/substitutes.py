"""Substitutes model of view helper"""


class SubstitutesHelper:

    def __init__(self, user):
        super().__init__(user)

    def records_concerned(self, category_id):
        """Tell if category exist in local connection table categories"""

        request = "SELECT DISTINCT fs.substitute_code  " \
                  "FROM food_substitutes AS fs, " \
                  "     food_categories AS fc " \
                  "WHERE  fc.food_code = fs.food_code " \
                  "AND fc.category_id = %s " \
                  "AND fs.user_id = %s ;"
        substitutes = []
        if self._user:
            values = (category_id, self._user.id)
            for row in self._connection.ask_request(request, values):
                substitutes.append(row["substitute_code"])
        return substitutes
