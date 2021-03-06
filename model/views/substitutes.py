"""Model for substitutes list view of Mainwindow"""

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtCore import Qt

from . import MixinModelsView
from settings import DEBUG_MODE



class SubstitutesModel(MixinModelsView, QStandardItemModel):
    """MainWindow substitutes view model"""

    def __init__(self, **kargs):
        kargs["parent"] = kargs["views"]["substitutes"]
        super().__init__(**kargs)
        self.setHorizontalHeaderLabels(["Nom", "Score", "Code"])
        self._checked = []

    def populate(self, foods, substitutes, page=0, new=True):
        """Return the list of possible substitution products inside
        substitutes list view without the selected one and for score better
        then selected one and without empty product_name substitutes"""

        selected = foods.selected
        user_state = self._user.is_connected() \
                     and not self._user.is_admin()
        if DEBUG_MODE:
            print("=====  S u b s t i t u t e s M o d e l  =====")
            print("Populate categories view")
            print("user is connected ?", user_state)
        if new:
            self.reset()
            if DEBUG_MODE:
                print("substitutes length:", len(substitutes))
        ldb_substitutes = []
        if user_state:
            ldb_substitutes = self._helper.records_concerned(foods.category_id)
            if DEBUG_MODE:
                print("categories found in Database:", ldb_substitutes)
        for food in substitutes[page]:
            checkable = bool(not self.is_in_database(
                    foods.category_id,
                    food["code"]) and user_state) \
                if self._general_ctrl.current_mode.name == \
                   "OpenFoodFactsMode" \
                else bool(self.is_in_database(
                    foods.category_id,
                    food["code"]) and user_state)
            if self.trash_dirty_product(food):
                del food
            else:
                target = food["nutrition_grades_tags"][0]
                if food["code"] != selected[0] \
                        and target <= selected[1]:
                    item_name = QStandardItem(food["product_name_fr"])
                    item_name.setCheckable(checkable)
                    item_grade = QStandardItem(
                        str(food["nutrition_grades_tags"][0]).upper())
                    item_grade.setTextAlignment(Qt.AlignCenter)
                    item_code = QStandardItem(food["code"])
                    if DEBUG_MODE:
                        print("populate:", food["product_name_fr"])
                    color_t = self._views["bg_color"]
                    color = QColor(color_t[0], color_t[1], color_t[2])
                    test_1 = "brands_tags" not in food.keys()
                    test_2 = "stores_tags" not in food or \
                             not food["stores_tags"]
                    if  test_1 and test_2:
                        color = QColor(255, 0, 0)
                    elif test_1:
                        color = QColor(255, 102, 0)
                    elif test_2:
                        color = QColor(255, 50, 0)
                    item_name.setBackground(color)
                    item_code.setBackground(color)
                    if food["code"] in ldb_substitutes:
                        item_name.setForeground(QColor(16, 133, 22))
                        item_code.setForeground(QColor(16, 133, 22))
                    else:
                        item_name.setForeground(QColor(0, 0, 0))
                        item_code.setForeground(QColor(0, 0, 0))
                    self.appendRow([item_name, item_grade, item_code])
        self.sort(1)

    def reset(self):
        """Reset model for substitutes_list view"""

        self._checked = []
        self.removeRows(0, self.rowCount())

    def update_checked(self, item, code):
        """Update checked list of codes from index selection"""

        if DEBUG_MODE:
            print("======  S u b s t i t u t e s M o d e l s  ======")
        if item.checkState() == Qt.Checked:
            self._checked.append(code)
            if DEBUG_MODE:
                print("checked list after add:", self._checked)
            return True
        else:
            if code in self._checked:
                self._checked.remove(code)
            if DEBUG_MODE:
                print("checked list after remove:", self._checked)
            return False

    def reset_checkboxes(self):
        """Un-check all checkboxes from item column 0 in this model
        of view"""

        for index in range(self.rowCount()):
            item = self.item(index, 0)
            if item.checkState() == Qt.Checked:
                item.setCheckState(Qt.Unchecked)
        self._checked = []

    def find_substitutes_in_database(self, selected_category):
        """Find and colored in green substitutes for user connected
        inside local database"""

        if self._user.is_connected() and not self._user.is_admin():
            for index in range(self.rowCount()):
                item_name = self.item(index, 0)
                item_code = self.item(index, 2)
                if self.is_in_database(selected_category,
                                      item_code.data()):
                    if DEBUG_MODE:
                        print("find item code:",
                              item_code.data(Qt.DisplayRole))
                    item_name.setCheckable(False)
                    item_name.setForeground(QColor(16, 133, 22))
                    item_code.setForeground(QColor(16, 133, 22))
                else:
                    item_name.setForeground(QColor(0, 0, 0))
                    item_code.setForeground(QColor(0, 0, 0))

    def is_in_database(self, category_id, code):
        """Find if this code is inside this category of products"""

        ldb_substitutes = self._helper.records_concerned(category_id)
        if code in ldb_substitutes:
            return True
        return False

    @property
    def checked(self):
        """Checked list of substitutes products property"""

        return self._checked
