"""Enumarators class are here"""

from enum import Enum


class Mode(Enum):
    """Selector cursor for item selected or item checkbox checked"""

    CHECKED = 1
    SELECTED_FOOD = 2
    SELECTED_SUBSTITUTE = 3
    KILLED = 4


class Widget(Enum):
    """Selection cursor for views or models to be reset"""

    ALL = 1
    CATEGORIES = 2
    FOODS = 3
    SUBSTITUTES = 4
    DETAILS = 5


class TypeConnection(Enum):
    """Type of connection"""

    ADMIN_CONNECTED = 1
    USER_CONNECTED = 2
    USER_DISCONNECTED = 3

