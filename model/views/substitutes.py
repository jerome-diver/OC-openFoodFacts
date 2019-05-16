'''Model for substitutes list view of Mainwindow'''

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor

class SubstitutesModel():
    '''Mainwindow substitutess view model'''

    def __init__(self, views):
        super().__init__(views)
        self._views = views
        self._substitutes = QStandardItemModel(self._views["substitutes"])
        self._substitutes.setHorizontalHeaderLabels(["Nom", "Grade", "Code"])
        self._selected_substitutes = []

    @property
    def substitutes(self):
        '''Substitutes list model'''

        return self._substitutes

    @property
    def selected_substitutes(self):
        '''Selected substitutes list (checked from substitutes list view)'''

        return self._selected_substitutes

    @selected_substitutes.setter
    def selected_substitutes(self, value):
        '''Set self._selected_substitutes'''

        self._selected_substitutes = value

    def populate_substitutes(self, food, page=0, new=True):
        '''Return the list of possible substitution products inside
        substitutes list view without the selected one and for score better
        then selected one and without empty product_name foods'''

        if new:
            self._substitutes.removeRows(0, self._substitutes.rowCount())
        for _food in self._foods_recorded[page]:
            if _food["product_name_fr"] != food \
                    and _food["nutrition_grades_tags"][0] != "not-applicable" \
                    and _food["nutrition_grades_tags"][0] <= \
                    self._selected_food[1]:
                item_name = QStandardItem(_food["product_name_fr"])
                item_name.setCheckable(True)
                item_grade = QStandardItem(_food["nutrition_grades_tags"][0])
                item_code = QStandardItem(_food["codes_tags"][1])
                color_t = self._views["bg_color"]
                color = QColor(color_t[0], color_t[1], color_t[2])
                test_1 = "brands_tags" not in _food.keys()
                test_2 = "stores_tags" not in _food or not _food["stores_tags"]
                if  test_1 and test_2:
                    color = QColor(255, 0, 0)
                elif test_1:
                    color = QColor(255, 102, 0)
                elif test_2:
                    color = QColor(255, 50, 0)
                item_name.setBackground(color)
                item_code.setBackground(color)
                self._substitutes.appendRow([item_name, item_grade, item_code])
        self._substitutes.sort(1)

    def reset_substitutes_list(self):
        '''Reset model for substitutes_list view'''

        self._selected_substitutes = []
        self._substitutes.removeRows(0, self._substitutes.rowCount())
