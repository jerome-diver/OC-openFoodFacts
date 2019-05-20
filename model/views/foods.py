"""Model for foods list view of Mainwindow"""

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor

from settings import DEBUG_MODE

class FoodsModel(QStandardItemModel):
    """Mainwindow foods view model"""

    def __init__(self, views, helper):
        super().__init__(views["foods"])
        self._views = views
        self._helper = helper
        self._recorded = [] # [ [] ]  |as pages of foods
        self._selected = ()
        self._category_id = None
        self._count = 0

    def populate(self, foods, new=True):
        """Return the list wiew of foods for give category string
        with openfoodfacts library helper"""

        ldb_foods = self._helper.records_concerned(self._category_id)
        if new:
            self.reset()
        for food in foods:
            key = "product_name_fr"
            if food[key].strip().isspace() or food[key] == '' and DEBUG_MODE:
                print("no way (no product name) for:", food["codes_tags"][1])
            else:
                self._count += 1
                name = QStandardItem(food[key].strip())
                code = QStandardItem(food["codes_tags"][1])
                score = QStandardItem(food["nutrition_grades_tags"][0])
                if code in ldb_foods:
                    name.setForeground(QColor(0, 250, 0))
                self.appendRow([name, code, score])
        self.sort(0)

    def reset(self):
        """Reset the foods list"""

        self._selected = ()
        self._count = 0
        self.removeRows(0, self.rowCount())

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
