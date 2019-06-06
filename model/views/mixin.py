"""Mixin class to share attributes and own Properties to use"""

from PyQt5.QtCore import Qt

from settings import DEBUG_MODE

class MixinModelsView():
    """Mix-ins class for share DRY properties of models-views:
    [categories, substitutes, foods]"""

    def __init__(self, **kargs):
        super().__init__(kargs["parent"])
        self._helper = kargs["helper"]
        self._general_ctrl = kargs["general_ctrl"]
        self._views = kargs["views"]
        self._user = self._general_ctrl.authenticate.user

    def flags(self, index):
        """Read only for QStandardItem.flags call override"""

        return Qt.ItemFlags(Qt.ItemIsEnabled + Qt.ItemIsSelectable)

    @staticmethod
    def trash_dirty_product(product):
        """Remove dirty product"""

        key = "product_name_fr"
        if key not in product:
            if DEBUG_MODE:
                print("no product_name_fr key ==> delete !",
                      product["code"])
            return True
        if product[key].isspace() or product[key] == '':
            if DEBUG_MODE:
                print("empty product_name_fr => delete ",
                      product["code"])
            return True
        key = "nutrition_grades_tags"
        if key not in product:
            if DEBUG_MODE:
                print("no nutrition_grades_tags => delete !",
                      product["code"])
            return True
        if product[key][0] == "not-applicable" or \
                product[key][0] == "unknown":
            if DEBUG_MODE:
                print("unknow or not-applicable nutrition_grades_tags => "
                      "delete !", product["code"])
            return True

    @property
    def helper(self):
        """Property helper access"""

        return self._helper

    @property
    def user(self):
        """Property for user access"""

        return self._user

    @user.setter
    def user(self, usr):
        """Setter property for user"""

        self._user = usr
        self._helper.user = usr
