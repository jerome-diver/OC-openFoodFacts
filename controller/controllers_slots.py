"""Slots for Controllers OpenFoodFactsMode and LocaleDatabaseMode"""

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from view import Messenger
from settings import DEBUG_MODE


class ControllerSlots(QObject):
    """Slots for controllers OpenFoodFactsMode and DatabaseMode"""

    def __init__(self, general_ctrl, controller):
        super().__init__()
        self._ctrl_general = general_ctrl
        self._ctrl = controller
        self._name = "%s" % type(controller).__name__
        self._messenger = Messenger(self._ctrl, self._ctrl.flags)
        self.connect()

    def __del__(self):
        """Auto disconnect at end life time"""

        self.disconnect()

    def connect(self):
        """Connect Signals with Slots"""

        if DEBUG_MODE:
            print("=====  C o n t r o l l e r S l o t  =====")
            print("connect similar connections")
        ######   Connect for controller   ##############################
        self._ctrl.views["categories"].clicked.connect(
            self._ctrl.on_category_selected)
        self._ctrl.views["foods"].clicked.connect(
            self._ctrl.on_food_selected)
        self._ctrl.views["substitutes"].selectionModel(). \
            selectionChanged.connect(
            self._ctrl.on_substitute_selection_changed)
        self._ctrl.model.substitutes.itemChanged.connect(
            self._ctrl.on_substitute_checked)
        self._ctrl.views["url"].clicked.connect(
            self._ctrl.on_product_url_clicked)
        self._ctrl.status_message.connect(
            self._ctrl.window.on_status_message)
        ######   Connect for messenger   ###############################
        self._ctrl.views["categories"].clicked.connect(
            self._messenger.on_category_selected)
        self._ctrl.views["foods"].clicked.connect(
            self._messenger.on_food_selected)
        self._ctrl.views["substitutes"].selectionModel(). \
            selectionChanged.connect(
            self._messenger.on_substitute_selection_changed)
        self._ctrl.model.substitutes.itemChanged.connect(
            self._messenger.on_substitute_checked)
        ######   Connect for general controller   ######################
        self._ctrl_general.user_event.connect(
            self._ctrl.model.on_user_event)
        self._ctrl.checked_start.connect(
            self._ctrl_general.on_checked_started)

        if self._name == "OpenFoodFactsMode":
            if DEBUG_MODE:
                print("Connect for OpenFoodFactsMode")
        ######   Connect for controller   ##############################
            self._ctrl.model.internet_access.connect(
                self._ctrl.on_internet_access)
            self._ctrl.load_categories.finished.connect(
                self._ctrl.on_load_categories_finished)
            self._ctrl.load_details_finished.connect(
                self._ctrl_general.on_load_details_finished)
        ######   Connect for messenger   ###############################
            self._ctrl.load_categories.finished.connect(
                self._messenger.on_load_categories_finished)
            self._ctrl.load_details_finished.connect(
                self._messenger.on_load_product_details_finished)
            self._ctrl.model.internet_access.connect(
                self._messenger.on_internet_access)

        elif self._name == "DatabaseMode":
            if DEBUG_MODE:
                print("Connect for DatabaseMode")

    def disconnect(self):
        """Disconnect SLots and Signals for Models linked"""
        
        if DEBUG_MODE:
            print("=====  C o n t r o l l e r S l o t  =====")
            print("disconnect similar connections")
        ######   Disconnect for controller   ###########################
        self._ctrl.views["categories"].clicked.disconnect(
            self._ctrl.on_category_selected)
        self._ctrl.views["foods"].clicked.disconnect(
            self._ctrl.on_food_selected)
        self._ctrl.views["substitutes"].selectionModel(). \
            selectionChanged.disconnect(
            self._ctrl.on_substitute_selection_changed)
        self._ctrl.model.substitutes.itemChanged.disconnect(
            self._ctrl.on_substitute_checked)
        self._ctrl.views["url"].clicked.disconnect(
            self._ctrl.on_product_url_clicked)
        self._ctrl.status_message.disconnect(
            self._ctrl.window.on_status_message)
        ######   Disconnect for messenger   ############################
        self._ctrl.views["categories"].clicked.disconnect(
            self._messenger.on_category_selected)
        self._ctrl.views["foods"].clicked.disconnect(
            self._messenger.on_food_selected)
        self._ctrl.views["substitutes"].selectionModel(). \
            selectionChanged.disconnect(
            self._messenger.on_substitute_selection_changed)
        self._ctrl.model.substitutes.itemChanged.disconnect(
            self._messenger.on_substitute_checked)
        ###### Disconnect for general controller
        self._ctrl_general.user_event.disconnect(
            self._ctrl.model.on_user_event)
        self._ctrl.checked_start.disconnect(
            self._ctrl_general.on_checked_started)

        if self._name == "OpenFoodFactsMode":
            if DEBUG_MODE:
                print("disconnect for OpenFoodFactsMode")
        ######   Connect for controller   ##############################
            self._ctrl.model.internet_access.disconnect(
                self._ctrl.on_internet_access)
            self._ctrl.load_categories.finished.disconnect(
                self._ctrl.on_load_categories_finished)
            self._ctrl.load_details_finished.disconnect(
                self._ctrl_general.on_load_details_finished)
        ######   Connect for messenger   ###############################
            self._ctrl.load_categories.finished.disconnect(
                self._messenger.on_load_categories_finished)
            self._ctrl.load_details_finished.disconnect(
                self._messenger.on_load_product_details_finished)
            self._ctrl.model.internet_access.disconnect(
                self._messenger.on_internet_access)

        elif self._name == "DatabaseMode":
            if DEBUG_MODE:
                print("disconnect for DatabaseMode")

