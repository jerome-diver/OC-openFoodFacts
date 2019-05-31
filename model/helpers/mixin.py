"""Mixin class for models-views helpers shared RDY code"""

class MixinHelpers:
    """Mixin models-view helpers"""

    def __init__(self, user):
        self._user = user
        self._connection = user.connection

    @property
    def user(self):
        """User property access"""

        return self._user

    @user.setter
    def user(self, usr):
        """Setter property for user"""

        self._user = usr
        self._connection = usr.connection
