"""Slots for Controllers OpenFoodFactsMode and LocaleDatabaseMode"""

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
import webbrowser

from enumerator import Mode
from view import Messenger
from . import ThreadsController, LoadCategories
from model import LocalDatabase, OpenFoodFacts
from settings import DEBUG_MODE


class MixinControllers(QObject):
    """Slots for controllers OpenFoodFactsMode and DatabaseMode"""

    status_message = pyqtSignal(str)
    checked_start = pyqtSignal()
    
    def __init__(self, **kargs):
        super().__init__()
        self._general_ctrl = kargs["general_ctrl"]
        self._name = "%s" % type(self).__name__
        self._window = self._general_ctrl.window
        self._authenticate = self._general_ctrl.authenticate
        self._connection = self._authenticate.user_connection
        self._flags = {"product": True,
                       "internet": True,
                       "call_mode": Mode.SELECTED}
        self._views = {"categories": self._window.categories_list,
                       "foods": self._window.foods_list,
                       "substitutes": self._window.substitutes_list,
                       "name" : self._window.product_name,
                       "brand" : self._window.product_brand,
                       "packaging" : self._window.product_packaging,
                       "code": self._window.product_code,
                       "score" : self._window.product_score,
                       "shops" : self._window.product_shops,
                       "description" : self._window.product_description,
                       "url" : self._window.product_url,
                       "img_thumb" : self._window.product_img_thumb,
                       "bg_color": self._window.get_bg_color()}
        if self._name == "OpenFoodFactsMode":
            self._model = OpenFoodFacts(general_ctrl=self._general_ctrl,
                                        views=self._views)
            self._threads = ThreadsController(self)
            self._load_categories = LoadCategories(
                self._model, self._connection)
        elif self._name == "DatabaseMode":
            self._model = LocalDatabase(general_ctrl=self._general_ctrl,
                                        views=self._views)
        self._messenger = Messenger(self, self._flags)
        self.connect()

    def __del__(self):
        """Auto disconnect at end life time"""

        #self.disconnect()

    def connect(self):
        """Connect Signals with Slots"""

        if DEBUG_MODE:
            print("=====  M i x i n C o n t r o l l e r s  =====")
            print("connect similar connections")
        ######   Connect for controller   ##############################
        self._views["categories"].clicked.connect(self.on_category_selected)
        self._views["foods"].clicked.connect(self.on_food_selected)
        self._views["substitutes"].selectionModel().selectionChanged.connect(
            self.on_substitute_selection_changed)
        self._model.substitutes.itemChanged.connect(self.on_substitute_checked)
        self._views["url"].clicked.connect(self.on_product_url_clicked)
        self.status_message.connect(self._window.on_status_message)
        ######   Connect for messenger   ###############################
        self._views["categories"].clicked.connect(
            self._messenger.on_category_selected)
        self._views["foods"].clicked.connect(
            self._messenger.on_food_selected)
        self._views["substitutes"].selectionModel().selectionChanged.connect(
            self._messenger.on_substitute_selection_changed)
        self._model.substitutes.itemChanged.connect(
            self._messenger.on_substitute_checked)
        ######   Connect for general controller   ######################
        self._general_ctrl.user_event.connect(self._model.on_user_event)
        self.checked_start.connect(self._general_ctrl.on_checked_started)

        if self._name == "OpenFoodFactsMode":
            if DEBUG_MODE:
                print("Connect for OpenFoodFactsMode")
        ######   Connect for controller   ##############################
            self._model.internet_access.connect(self.on_internet_access)
            self._load_categories.finished.connect(
                self.on_load_categories_finished)
            self.load_details_finished.connect(
                self._general_ctrl.on_load_details_finished)
        ######   Connect for messenger   ###############################
            self._load_categories.finished.connect(
                self._messenger.on_load_categories_finished)
            self.load_details_finished.connect(
                self._messenger.on_load_product_details_finished)
            self._model.internet_access.connect(
                self._messenger.on_internet_access)

        elif self._name == "DatabaseMode":
            if DEBUG_MODE:
                print("Connect for DatabaseMode")

    def disconnect(self):
        """Disconnect SLots and Signals for Models linked"""
        
        if DEBUG_MODE:
            print("=====  M i x i n C o n t r o l l e r s  =====")
            print("disconnect similar connections")
        ######   Disconnect for controller   ###########################
        self._views["categories"].clicked.disconnect(self.on_category_selected)
        self._views["foods"].clicked.disconnect(self.on_food_selected)
        self._views["substitutes"].selectionModel(). \
            selectionChanged.disconnect(
            self.on_substitute_selection_changed)
        self._model.substitutes.itemChanged.disconnect(
            self.on_substitute_checked)
        self._views["url"].clicked.disconnect(self.on_product_url_clicked)
        self.status_message.disconnect(self._window.on_status_message)
        ######   Disconnect for messenger   ############################
        self._views["categories"].clicked.disconnect(
            self._messenger.on_category_selected)
        self._views["foods"].clicked.disconnect(
            self._messenger.on_food_selected)
        self._views["substitutes"].selectionModel(). \
            selectionChanged.disconnect(
            self._messenger.on_substitute_selection_changed)
        self._model.substitutes.itemChanged.disconnect(
            self._messenger.on_substitute_checked)
        ###### Disconnect for general controller
        self._general_ctrl.user_event.disconnect(self._model.on_user_event)
        self.checked_start.disconnect(
            self._general_ctrl.on_checked_started)

        if self._name == "OpenFoodFactsMode":
            if DEBUG_MODE:
                print("disconnect for OpenFoodFactsMode")
        ######   Connect for controller   ##############################
            self._model.internet_access.disconnect(self.on_internet_access)
            self._load_categories.finished.disconnect(
                self.on_load_categories_finished)
            self.load_details_finished.disconnect(
                self._general_ctrl.on_load_details_finished)
        ######   Connect for messenger   ###############################
            self._load_categories.finished.disconnect(
                self._messenger.on_load_categories_finished)
            self.load_details_finished.disconnect(
                self._messenger.on_load_product_details_finished)
            self._model.internet_access.disconnect(
                self._messenger.on_internet_access)

        elif self._name == "DatabaseMode":
            if DEBUG_MODE:
                print("disconnect for DatabaseMode")

    @pyqtSlot()
    def on_product_url_clicked(self):
        """Go to url"""

        url = self._model.product_details.models["url"]
        webbrowser.open(url)

    @property
    def model(self):
        """Return model property for OpenFoodFacts instance model"""

        return self._model

    @property
    def connection(self):
        """connection property access"""

        return self._connection

    @property
    def window(self):
        """Window access property"""

        return self._window

    @property
    def views(self):
        """Views property access"""

        return self._views

    @property
    def flags(self):
        """Property for flags access"""

        return self._flags
