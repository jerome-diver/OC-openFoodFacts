"""Share some methods there for descendant class to be DRY"""

from PyQt5.QtCore import pyqtSlot, QObject


class MixinSigns(QObject):
    """Share methods"""

    def __init__(self, **kargs):
        super().__init__()

    @pyqtSlot()
    def on_reset_status(self):
        """Reset status and bg color for status and username edit line"""

        stylesheet = "background-color: rgba(0,0,0,0); color: black;"
        self.setup_widget(stylesheet)
        self.status.setText("")

    @pyqtSlot(str)
    def on_status(self, message):
        """Print a status message to status label QObject of QDialog"""

        stylesheet = "color: red; background-color: rgba(20,20,20,0.7);"
        self.setup_widget(stylesheet)
        self.status.setText(message)

    def setup_widget(self, stylesheet):
        """Setup widgets status and username stylesheet"""

        self.status.setStyleSheet(stylesheet)
        self.username.setStyleSheet(stylesheet)
