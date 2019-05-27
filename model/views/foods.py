"""Model for foods list view of Mainwindow"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor

from . import MixinViews
from settings import DEBUG_MODE


class FoodsModel(MixinViews, QStandardItemModel):
    """Mainwindow foods view model"""

    def __init__(self, **kargs):
        kargs["parent"] = kargs["views"]["foods"]
        super().__init__(**kargs)
        self._recorded = [] # [ [] ]  |as pages of foods
        self._selected = ()
        self._selected_details = dict()
        self._category_id = None
        self._count = 0

    def populate(self, foods, new=True):
        """Return the list wiew of foods for give category string
        with openfoodfacts library helper"""

        user_state = self._user.is_connected()
        if DEBUG_MODE:
            print("=====  F o o d s M o d e l  =====")
            print("Populate categories view")
            print("user is connected ?", user_state)
        ldb_foods = []
        if user_state:
            ldb_foods = self._helper.records_concerned(self._category_id)
            if DEBUG_MODE:
                print("categories found in Database:", ldb_foods)
        if new:
            self.reset()
        for food in foods:
            key = "product_name_fr"
            if key not in food:
                del food
            elif food[key].isspace() or food[key] == '':
                if DEBUG_MODE:
                    print("no way (no product name) for:", food["code"])
                del food
            else:
                self._count += 1
                name = QStandardItem(food[key].strip())
                code = QStandardItem(food["code"])
                score = QStandardItem(food["nutrition_grades_tags"][0])
                if food["code"] in ldb_foods:
                    name.setForeground(QColor(16, 133, 22))
                else:
                    name.setForeground(QColor(0, 0, 0))
                self.appendRow([name, code, score])
        self.sort(0)

    def reset(self):
        """Reset the foods list"""

        self._selected = ()
        self._count = 0
        self.removeRows(0, self.rowCount())

    def find_foods_in_database(self):
        """Find and colored in green foods for user connected inside local
        database"""

        user_state = self._user.is_connected()
        if user_state:
            ldb_foods = self._helper.records_concerned(self._category_id)
            for index in range(self.rowCount()):
                item_name = self.item(index, 0)
                item_code = self.item(index, 1)
                if item_code.data(Qt.DisplayRole) in ldb_foods:
                    if DEBUG_MODE:
                        print("find item code:",
                              item_code.data(Qt.DisplayRole))
                    item_name.setForeground(QColor(16, 133, 22))
                else:
                    item_name.setForeground(QColor(0, 0, 0))

    @property
    def selected_details(self):
        """Selected food details food (from food list view)"""

        return self._selected_details

    @selected_details.setter
    def selected_details(self, value):
        """Setter for property of dict selected food details"""

        self._selected_details = value

    @property
    def selected(self):
        """Selected food (from food list view)"""

        return self._selected

    @selected.setter
    def selected(self, value):
        """Setter for property of tuple selected_food"""

        self._selected = value

    @property
    def category_id(self):
        """Selected food (from food list view)"""

        return self._category_id

    @category_id.setter
    def category_id(self, value):
        """Setter for property of tuple selected_food"""

        self._category_id = value

    @property
    def recorded(self):
        """Recorded foods list by page found property"""

        return self._recorded

    @recorded.setter
    def recorded(self, value):
        """Setter for recorded values"""

        self._recorded = value

    @property
    def count(self):
        """Count foods property"""

        return self._count

    @count.setter
    def count(self, value):
        """Setter count property"""

        self._count = value
