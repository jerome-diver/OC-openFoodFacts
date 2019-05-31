"""Messenger send messages in the view"""

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QItemSelection, \
                        QModelIndex

from enumerator import Mode
from settings import DEBUG_MODE


class Messenger(QObject):
    """Show message on screen with status bar and dialog boxes"""

    status_message = pyqtSignal(str)

    def __init__(self, controller, flags):
        super().__init__()
        self._ctrl = controller
        self._flags = flags

    @pyqtSlot()
    def on_load_categories_finished(self):
        """Show categories of products food
        from openFoodFacts model in view"""

        self.status_message.emit("Effectuez une recherche sur Open Food "
                                 "Facts ou authentifiez vous pour accéder "
                                 "à vôtre base de données")

    @pyqtSlot()
    def on_load_foods_finished(self):
        """Show food's products from Open Food Facts"""

        if self._flags["product"]:
            self.status_message.emit("Tous les produits de la catégorie sont "
                                     "affichés")
        if DEBUG_MODE:
            print("=====  M e s s e n g e r  =====")
            print("End process to load foods")

    @pyqtSlot(int, int)
    def on_new_food_page(self, page, total):
        """Reload the view for new page added"""

        self.status_message.emit("Affichage des produits en cours... "
                                 "pages: {} affichées | {} restantes".
                                 format(page, total))
        if DEBUG_MODE:
            print("=====  M e s s e n g e r  =====")
            print("selected food already for:",
                  self._ctrl.model.foods.selected)

    @pyqtSlot()
    def on_load_product_details_finished(self):
        """Show details of product from Open Food Facts"""

        if self._flags["call_mode"] is Mode.CHECKED:
            self.status_message.emit("Détails des substituts sélectionnés "
                                     "trouvés")
        else:
            self.status_message.emit("Détails du substitut choisi affiché")

    @pyqtSlot()
    def on_no_product_found(self):
        """When no product found for category selected happening..."""

        if self._flags["internet"]:
            self.status_message.emit("Il n'y a aucun produit pour cette catégorie")

    @pyqtSlot(bool)
    def on_internet_access(self, status):
        """When no internet access is happening..."""

        if not status:
            self.status_message.emit("Il n'y a pas d'accès à internet")
            if DEBUG_MODE:
                print("=====  M e s s e n g e r  =====")
                print("there is no internet access")

    @pyqtSlot(QModelIndex)
    def on_category_selected(self, index):
        """Slot for next action on clicked category selection from
        category list view"""

        self.status_message.emit("Patientez, recherche des produits "
                                 "relatifs à la catégorie en cours "
                                 "sur Open Food Facts...")

    @pyqtSlot(QModelIndex)
    def on_food_selected(self, index):
        """Slot for next action on clicked foods selection from
        foods list view"""

        self._flags["product"] = False
        self.status_message.emit("Patientez, recherche des produits "
                                 "de substitutions proposés en cours "
                                 "sur Open Food Facts...")

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_substitute_selection_changed(self, selected, deselected):
        """Load details from new selection of substitutes table view"""

        if selected.indexes():
            index = selected.indexes()[0]
            sub_model = self._ctrl._views["substitutes"].model()
            code = sub_model.index(index.row(), 2).data()
            name = sub_model.index(index.row(), 0).data()
            if DEBUG_MODE:
                print("=====  M e s s e n g e r  =====")
                print("now searching product for code", code,
                      "name", name)
            self.status_message.emit("Patientez, recherche sur le code "
                                     "produit {} sélectionné".format(code))

    @pyqtSlot('QStandardItem*')
    def on_substitute_checked(self, item):
        """Load, from checkbox (substitutes table view) selected, products
        details"""

        index = self._ctrl.model.substitutes.indexFromItem(item)
        code = self._ctrl.model.substitutes.index(index.row(), 2).data()
        name = self._ctrl._model.substitutes.index(index.row(), 0).data()
        if DEBUG_MODE:
            print("=====  M e s s e n g e r  =====")
            print("now searching product for code", code, "name", name)
        self.status_message.emit("Patientez, recherche sur le code produit "
                                 "{} à ajouter dans la base".format(code))
