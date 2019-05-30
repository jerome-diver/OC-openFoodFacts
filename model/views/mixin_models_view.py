"""Mixin class to share attributes and own Properties to use"""


class MixinModelsView():
    """Mix-ins class for share DRY properties of models-views:
    [categories, substitutes, foods]"""

    def __init__(self, **kargs):
        super().__init__(kargs["parent"])
        self._helper = kargs["helper"]
        self._general_ctrl = kargs["general_ctrl"]
        self._views = kargs["views"]
        self._user = self._general_ctrl.authenticate.user

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
