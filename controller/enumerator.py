"""Enumarators class are here"""

from enum import Enum


class Mode(Enum):
    """Selector cursor for item selected or item checkbox checked"""

    CHECKED = 1
    SELECTED = 2
    GET = 3


class Widget(Enum):
    """Selection cursor for views or models to be reset"""

    ALL = 1
    CATEGORIES = 2
    FOODS = 3
    SUBSTITUTES = 4
    DETAILS = 5
