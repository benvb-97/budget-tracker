from typing import TYPE_CHECKING

from PySide6.QtCore import QItemSelectionModel, QModelIndex, Qt, QSize
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
from src.models.TransactionCSVReaders import TransactionCSVReadersOverviewModel
from src.ui.delegates.SpinBoxDelegate import SpinBoxDelegate

if TYPE_CHECKING:
    from src.models.Projects import ProjectsModel


class ReadersTableView(QTableView):
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
            model: TransactionCSVReadersOverviewModel = index.model()

            menu = QMenu(self)

            # Add actions to the context menu
            delete_action = QAction("Delete reader", self)
            delete_action.triggered.connect(lambda: model.delete_item(index))
            menu.addAction(delete_action)

            # Show the menu at the cursor position
            menu.exec(self.viewport().mapToGlobal(position))


class ReadersDialog(QDialog):
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

        self._readers_view.resizeColumnsToContents()
        self.resize(QSize(600, 400))

    def _setup_ui(self) -> None:
        self.setWindowTitle("Manage Transaction CSV Readers")
        self._layout = QVBoxLayout(self)

        # Table view
        self._readers_view = ReadersTableView(self)
        self._readers_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems
        )
        self._readers_view.setHorizontalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self._readers_view.setAlternatingRowColors(True)

        for col in (TransactionCSVReadersOverviewModel.cols.DATE_COLUMN,
                    TransactionCSVReadersOverviewModel.cols.NOTE_COLUMN,
                    TransactionCSVReadersOverviewModel.cols.ACCOUNT_COLUMN,
                    TransactionCSVReadersOverviewModel.cols.AMOUNT_COLUMN,
                    TransactionCSVReadersOverviewModel.cols.COUNTERPART_COLUMN,):
            delegate = SpinBoxDelegate(lbound=0, ubound=999, parent=self)
            self._readers_view.setItemDelegateForColumn(col, delegate)

        self._header_view = QHeaderView(Qt.Orientation.Horizontal, self._readers_view)
        self._header_view.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self._header_view.setStretchLastSection(True)
        self._readers_view.setHorizontalHeader(self._header_view)

        # New Reader button
        self._new_reader_button = QPushButton("New Reader", self)

        # Add widgets to layout
        self._layout.addWidget(self._readers_view)
        self._layout.addStretch()
        self._layout.addWidget(self._new_reader_button)


    def _set_models(self) -> None:
        self._readers_model = self._projects_model.transaction_csv_readers_model

        self._readers_list_selection_model = QItemSelectionModel(self._readers_model)

        self._readers_view.setModel(self._readers_model)
        self._readers_view.setSelectionModel(self._readers_list_selection_model)

    def _setup_connections(self) -> None:
        self._readers_list_selection_model.selectionChanged.connect(
            self._readers_model.change_selection
        )

        self._new_reader_button.clicked.connect(self._readers_model.create_new_item)