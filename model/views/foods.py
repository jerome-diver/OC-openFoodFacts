'''Model for foods list view of Mainwindow'''

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from settings import DEBUG_MODE

class FoodsModel():
    '''Mainwindow foods view model'''

    def __init__(self, views):
        super().__init__(views)
        self._views = views
        self._foods = QStandardItemModel(self._views["foods"])
        self._foods_recorded = [] # [ [] ]  |as pages of foods
        self._selected_food = ()

    @property
    def foods(self):
        '''Foods list model'''

        return self._foods

    @property
    def selected_food(self):
        '''Selected food (from food list view)'''

        return self._selected_food

    @selected_food.setter
    def selected_food(self, value):
        '''Setter for property of tuple selected_food'''

        self._selected_food = value

    def populate_foods(self, foods, new=True):
        '''Return the list wiew of foods for give category string
        with openfoodfacts library helper'''

        if new:
            self.reset_foods_list()
        for food in foods:
            key = "product_name_fr"
            if food[key].strip().isspace() or food[key] == '' and DEBUG_MODE:
                print("no way (no product name) for:", food["codes_tags"][1])
            else:
                name = QStandardItem(food[key].strip())
                code = QStandardItem(food["codes_tags"][1])
                score = QStandardItem(food["nutrition_grades_tags"][0])
                self._foods.appendRow([name, code, score])
        self._foods.sort(0)

    def reset_foods_list(self):
        '''Reset the foods list'''

        self._selected_food = ()
        self._foods.removeRows(0, self._foods.rowCount())
