"""Slots Models for OpenFoodFacts and LocalDatabaase"""

from PyQt5.QtCore import QObject, pyqtSlot

from model import User
from settings import DEBUG_MODE


class SlotsModels(QObject):

    def __init__(self, model):
        super().__init__()
        self._model = model
        self._name = "%s" % type(model).__name__

    @pyqtSlot(User)
    def on_user_event(self, user):
        """When a user is connected"""

        if DEBUG_MODE:
            print("=====  S l o t M o d e l s  (", self._name,")  =====")
            print("config for User connected:", user.username)
        self._model.connection = user.connection
        self._model.user = user
        self._model.categories.user = user
        self._model.foods.user = user
        self._model.substitutes.user = user
        if self._model.categories.rowCount():
            self._model.categories.find_categories_in_database()
        if self._model.foods.rowCount():
            self._model.foods.find_foods_in_database()
        if self._model.substitutes.rowCount():
            self._model.substitutes.find_substitutes_in_database(
                self._model.foods.category_id)
