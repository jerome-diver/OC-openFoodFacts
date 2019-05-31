"""Slots Models for OpenFoodFacts and LocalDatabase"""

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from . import User
from . import CategoriesModel, FoodsModel, \
    SubstitutesModel, ProductDetailsModels
from . import CategoriesHelper, FoodsHelper, SubstitutesHelper
from controller import Widget
from settings import DEBUG_MODE


class MixinModels(QObject):
    """Slots shared for models of views"""

    internet_access = pyqtSignal(bool)

    def __init__(self, **kargs):
        super().__init__()
        self._name = "%s" % type(self).__name__
        if "general_ctrl" not in kargs:
            self._user = None
            self._substitutes = None
            self._foods = None
            self._categories = None
            self._product_details = None
        else:
            self._authenticate = kargs["general_ctrl"].authenticate
            self._user = self._authenticate.user
            self._connection = self._user.connection
            self._views = kargs["views"]
            self._categories = CategoriesModel(
                general_ctrl=kargs["general_ctrl"], views=self._views,
                helper=CategoriesHelper(self._user))
            self._foods = FoodsModel(
                general_ctrl=kargs["general_ctrl"], views=self._views,
                helper=FoodsHelper(self._user))
            self._substitutes = SubstitutesModel(
                general_ctrl=kargs["general_ctrl"], views=self._views,
                helper=SubstitutesHelper(self._user))
            self._product_details = ProductDetailsModels(self._views)

    @pyqtSlot(User)
    def on_user_event(self, user):
        """When a user is connected"""

        if DEBUG_MODE:
            print("=====  S l o t M o d e l s  (", self._name,")  =====")
            print("config for User connected:", user.username)
        self._connection = user.connection
        self._user = user
        self._categories.user = user
        self._foods.user = user
        self._substitutes.user = user
        self.refresh_views_colors()

    def refresh_views_colors(self):
        """Refresh all views colored local database existing items"""

        if self._categories.rowCount():
            self._categories.find_categories_in_database()
        if self._foods.rowCount():
            self._foods.find_foods_in_database()
        if self._substitutes.rowCount():
            self._substitutes.find_substitutes_in_database(
                self._foods.category_id)

    def reset_models(self, models=(Widget.ALL,)):
        """Reset all models or elected ones"""

        if Widget.CATEGORIES in models or Widget.ALL in models:
            self._categories.reset()
        if Widget.FOODS in models or Widget.ALL in models:
            self._foods.reset()
        if Widget.SUBSTITUTES in models or Widget.ALL in models:
            self._substitutes.reset()
        if Widget.DETAILS in models or Widget.ALL in models:
            self._product_details.reset()

    @property
    def categories(self):
        """Categories property"""

        return self._categories

    @property
    def foods(self):
        """Foods property"""

        return self._foods

    @property
    def substitutes(self):
        """Substitutes property"""

        return self._substitutes

    @property
    def product_details(self):
        """Product details property"""

        return self._product_details

    @property
    def connection(self):
        """Property _connection access"""

        return self._connection

    @connection.setter
    def connection(self, new_connection):
        """Setter for self._connection"""

        self._connection = new_connection
