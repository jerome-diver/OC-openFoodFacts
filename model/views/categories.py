"""Model of "categories" Mainwindow view"""

import re

from PyQt5.QtGui import QStandardItemModel, QStandardItem

class CategoriesModel(QStandardItemModel):
    """categories view model"""

    def __init__(self, views):
        super().__init__(views["categories"])
        self._views = views
        self._selected = None

    @property
    def selected(self):
        """Return selected category"""

        return self._selected

    @selected.setter
    def selected(self, value):
        """Setter property for _selected_category"""

        self._selected = value


    def populate(self, categories):
        """Return all categories inside list categories view
        by openfoodfacts module helper"""

        self.removeRows(0, self.rowCount())
        self._selected = None
        for category in categories:
            is_fr = re.match(r'^fr:', category["name"])
            is_latin_chars = re.match(r'[0-9a-zA-z\s]', category["name"])
            if is_latin_chars:
                name = re.sub(r'^fr:', '', category["name"]) if is_fr \
                    else category["name"]
                item_name = QStandardItem(name)
                item_id = QStandardItem(category["id"])
                item_off_name = QStandardItem(category["name"])
                self.appendRow([item_name, item_id, item_off_name])

    def reset(self):
        """Reset the foods list"""

        self._selected = None
        self.removeRows(0, self.rowCount())
