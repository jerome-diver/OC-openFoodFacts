'''QLabel but with click event signal from mouse click'''

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel

class QLabelClickable(QLabel):
    '''QLabel + clicked signal event for mouse click'''

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)

    def mousePressEvent(self, ev):
        '''Event from mouse click'''

        self.clicked.emit()