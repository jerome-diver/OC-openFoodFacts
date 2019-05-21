"""Model for substitutes list view of Mainwindow"""

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtCore import Qt

from settings import DEBUG_MODE

class SubstitutesModel(QStandardItemModel):
    """MainWindow substitutes view model"""

    def __init__(self, views, helper):
        super().__init__(views["substitutes"])
        self.setHorizontalHeaderLabels(["Nom", "Grade", "Code"])
        self._views = views
        self._helper = helper
        self._checked = []

    @property
    def checked(self):
        """Checked list of substitutes products property"""

        return self._checked

    def populate(self, selected, foods, page=0, new=True):
        """Return the list of possible substitution products inside
        substitutes list view without the selected one and for score better
        then selected one and without empty product_name foods"""

        if new:
            self.reset()
            if DEBUG_MODE:
                print("foods length:", len(foods))
        ldb_substitutes = self._helper.records_concerned(selected[0])
        for food in foods[page]:
            if food["codes_tags"][1] != selected[0] \
                    and food["nutrition_grades_tags"][0] != "not-applicable" \
                    and food["nutrition_grades_tags"][0] <= selected[1]:
                item_name = QStandardItem(food["product_name_fr"])
                item_name.setCheckable(True)
                item_grade = QStandardItem(food["nutrition_grades_tags"][0])
                item_code = QStandardItem(food["codes_tags"][1])
                color_t = self._views["bg_color"]
                color = QColor(color_t[0], color_t[1], color_t[2])
                test_1 = "brands_tags" not in food.keys()
                test_2 = "stores_tags" not in food or not food["stores_tags"]
                if  test_1 and test_2:
                    color = QColor(255, 0, 0)
                elif test_1:
                    color = QColor(255, 102, 0)
                elif test_2:
                    color = QColor(255, 50, 0)
                item_name.setBackground(color)
                item_code.setBackground(color)
                if food["codes_tags"][1] in ldb_substitutes:
                    item_name.setForeground(QColor(0, 250, 0))
                self.appendRow([item_name, item_grade, item_code])
        self.sort(1)

    def reset(self):
        """Reset model for substitutes_list view"""

        self._checked = []
        self.removeRows(0, self.rowCount())

    def generate_checked(self):
        """Update list of checked item codes"""

        self._checked = []
        for index in range(self.rowCount()):
            item = self.item(index, 0)
            code = self.item(index, 2).text()
            if item.checkState() == Qt.Checked:
                self._checked.append(code)
        if DEBUG_MODE:
            print("checked list:", self._checked)

    def reset_checkboxes(self):
        """Un-check all checkboxes from item column 0 in this model
        of view"""

        for index in range(self.rowCount()):
            item = self.item(index, 0)
            if item.checkState() == Qt.Checked:
                item.setCheckState(Qt.Unchecked)