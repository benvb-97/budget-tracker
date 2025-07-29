from typing import TYPE_CHECKING

from PySide6.QtCore import QItemSelectionModel, QModelIndex, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QListView, QTableView,
    QMenu,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget, QHeaderView
)

from src.data.settings.AppSettings import AppSettings

if TYPE_CHECKING:
    from src.models.Projects import ProjectsModel
from src.models.TransactionCategories import TransactionCategoriesOverviewModel


class CategoriesTableView(QTableView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)

    def open_context_menu(self, position):
        """
        Opens at right-click
        """
        index = self.indexAt(position)  # type: QModelIndex

        if index.isValid():
            model: TransactionCategoriesOverviewModel = index.model()

            menu = QMenu(self)

            # Add actions to the context menu
            delete_action = QAction("Delete category", self)
            delete_action.triggered.connect(lambda: model.delete_item(index))
            menu.addAction(delete_action)

            # Show the menu at the cursor position
            menu.exec(self.viewport().mapToGlobal(position))


class CategoriesDialog(QDialog):
    def __init__(self,
                 projects_model: "ProjectsModel",
                 settings: AppSettings,
                 parent):
        super().__init__(parent)

        self._projects_model = projects_model
        self._settings = settings

        self._setup_ui()
        self._set_models()
        self._setup_connections()

    def _setup_ui(self) -> None:
        self.setWindowTitle("Manage Transaction Categories")
        self._layout = QVBoxLayout(self)

        # List view
        self._categories_view = CategoriesTableView(self)
        self._categories_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems
        )
        self._categories_view.setHorizontalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self._categories_view.setAlternatingRowColors(True)

        self._header_view = QHeaderView(Qt.Orientation.Horizontal, self._categories_view)
        self._header_view.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self._header_view.setStretchLastSection(True)
        self._categories_view.setHorizontalHeader(self._header_view)

        # New Category button
        self._new_category_button = QPushButton("New Category", self)

        # Add widgets to layout
        self._layout.addWidget(self._categories_view)
        self._layout.addStretch()
        self._layout.addWidget(self._new_category_button)


    def _set_models(self) -> None:
        self._categories_model = self._projects_model.transaction_categories_model

        self._categories_list_selection_model = QItemSelectionModel(self._categories_model)

        self._categories_view.setModel(self._categories_model)
        self._categories_view.setSelectionModel(self._categories_list_selection_model)

    def _setup_connections(self) -> None:
        self._categories_list_selection_model.selectionChanged.connect(
            self._categories_model.change_selection
        )

        self._new_category_button.clicked.connect(self._categories_model.create_new_item)