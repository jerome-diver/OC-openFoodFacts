'''Share some methods there for descendant class to be DRY'''

from PyQt5.QtCore import pyqtSlot, QObject

class Share(QObject):
    '''Share methods'''

    @pyqtSlot()
    def on_reset_status(self):
        '''Reset status and bg color for status and username edit line'''

        stylesheet = "background-color: rgba(0,0,0,0); color: black;"
        self.status.setStyleSheet(stylesheet)
        self.username.setStyleSheet(stylesheet)
        self.status.setText("")

    @pyqtSlot(str)
    def on_status(self, message):
        '''Print a status message to status label QObject of QDialog'''

        stylesheet = "color: red; background-color: rgba(20,20,20,0.7);"
        self.status.setStyleSheet(stylesheet)
        self.username.setStyleSheet(stylesheet)
        self.status.setText(message)
