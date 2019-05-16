'''Model of "categories" Mainwindow view'''

import re

from PyQt5.QtGui import QStandardItemModel, QStandardItem

class CategoriesModel():
    '''categories view model'''

    def __init__(self, views):
        super().__init__(views)
        self._views = views
        self._selected_category = None
        self._categories = QStandardItemModel(self._views['categories'])

    @property
    def categories(self):
        '''categories list model'''

        return self._categories

    @property
    def selected_category(self):
        '''Return selected category'''

        return self._selected_category

    @selected_category.setter
    def selected_category(self, value):
        '''Setter property for _selected_category'''

        self._selected_category = value


    def populate_categories(self, categories):
        '''Return all categories inside list categories view
        by openfoodfacts module helper'''

        self._categories.removeRows(0, self._categories.rowCount())
        self._foods_recorded = []
        for category in categories:
            is_fr = re.match(r'^fr:', category["name"])
            is_latin_chars = re.match(r'[0-9a-zA-z\s]', category["name"])
            if is_latin_chars:
                name = re.sub(r'^fr:', '', category["name"]) if is_fr \
                    else category["name"]
                item_name = QStandardItem(name)
                item_id = QStandardItem(category["id"])
                item_off_name = QStandardItem(category["name"])
                self._categories.appendRow([item_name, item_id, item_off_name])
