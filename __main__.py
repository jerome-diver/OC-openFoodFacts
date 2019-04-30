'''Main program for openFoodFacts substitution search food'''

import os, sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.ui_mainwindow import Ui_MainWindow
from controller import Authentication, DatabaseMode, OpenFoodFactsMode

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
