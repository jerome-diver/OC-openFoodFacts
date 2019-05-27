"""Mixin class to share attributes and own Propêrties to use"""


class MixinViews():

    def __init__(self, general_ctrl, views=None, helper=None,
                 **kargs):
        super().__init__(**kargs)
        self._helper = helper
        self._general_ctrl = general_ctrl
        self._views = views
        self._user = general_ctrl.authenticate.user

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
