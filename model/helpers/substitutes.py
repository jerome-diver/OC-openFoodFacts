"""Substitutes model of view helper"""


class SubstitutesHelper:

    def __init__(self, database, user):
        self._database = database
        self._user = user

    def records_concerned(self, food_code):
        """Tell if category exist in local database table categories"""

        request = "SELECT DISTINCT fs.substitute_code  " \
                  "FROM food_substitutes AS fs, user_foods AS uf " \
                  "WHERE  uf.food_code = fs.food_code " \
                  "AND uf.user_id = %s " \
                  "AND fs.food_code = %s ;"
        substitutes = []
        if self._user:
            values = (self._user.id, food_code)
            for row in self._database.ask_request(request, values):
                substitutes.append(row["substitute_code"])
        return substitutes

    @property
    def user(self):
        """User property access"""

        return self._user

    @user.setter
    def user(self, value):
        """Setter property for user"""

        self._user = value
