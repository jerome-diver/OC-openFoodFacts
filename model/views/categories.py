"""Model of "categories" Mainwindow view"""

import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor

from settings import DEBUG_MODE


class CategoriesModel(QStandardItemModel):
    """categories view model"""

    def __init__(self, views, helper):
        super().__init__(views["categories"])
        self._views = views
        self._helper = helper

    def populate(self, categories):
        """Return all categories inside list categories view
        by openfoodfacts module helper"""

        self.removeRows(0, self.rowCount())
        ldb_categories = self._helper.records_concerned()
        for category in categories:
            is_fr = re.match(r'^fr:', category["name"])
            is_latin_chars = re.match(r'[0-9a-zA-z\s]', category["name"])
            if is_latin_chars:
                name = re.sub(r'^fr:', '', category["name"]) if is_fr \
                    else category["name"]
                item_name = QStandardItem(name)
                item_id = QStandardItem(category["id"])
                item_off_name = QStandardItem(category["name"])
                if category["id"] in ldb_categories:
                    item_name.setForeground(QColor(0, 250, 0))
                self.appendRow([item_name, item_id, item_off_name])
        self.sort(0)

    def reset(self):
        """Reset the foods list"""

        self.removeRows(0, self.rowCount())

    def find_categories_in_database(self):
        """Find and colored in green foods for user connected inside local
        database"""

        ldb_categories = self._helper.records_concerned()
        for index in range(self.rowCount()):
            item_name = self.item(index, 0)
            item_code = self.item(index, 1)
            if item_code.data(Qt.DisplayRole) in ldb_categories:
                if DEBUG_MODE:
                    print("find item code:",
                          item_code.data(Qt.DisplayRole))
                item_name.setForeground(QColor(16, 133, 22))

    @property
    def helper(self):
        """Property helper access"""

        return self._helper
