'''Model for foods list view of Mainwindow'''

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from settings import DEBUG_MODE

class FoodsModel(QStandardItemModel):
    '''Mainwindow foods view model'''

    def __init__(self, views):
        super().__init__(views["foods"])
        self._views = views
        self._recorded = [] # [ [] ]  |as pages of foods
        self._selected = ()
        self._recorded = []
        self._count = 0

    @property
    def selected(self):
        '''Selected food (from food list view)'''

        return self._selected

    @selected.setter
    def selected(self, value):
        '''Setter for property of tuple selected_food'''

        self._selected = value

    @property
    def recorded(self):
        '''Recorded foods list by page found property'''

        return self._recorded

    @property
    def count(self):
        '''Count foods property'''

        return self._count

    @count.setter
    def count(self, value):
        '''Setter count property'''

        self._count = value

    def populate(self, foods, new=True):
        '''Return the list wiew of foods for give category string
        with openfoodfacts library helper'''

        if new:
            self.reset()
        for food in foods:
            key = "product_name_fr"
            if food[key].strip().isspace() or food[key] == '' and DEBUG_MODE:
                print("no way (no product name) for:", food["codes_tags"][1])
            else:
                name = QStandardItem(food[key].strip())
                code = QStandardItem(food["codes_tags"][1])
                score = QStandardItem(food["nutrition_grades_tags"][0])
                self.appendRow([name, code, score])
        self.sort(0)

    def reset(self):
        '''Reset the foods list'''

        self._selected = ()
        self.removeRows(0, self.rowCount())
