from typing import TYPE_CHECKING

from PySide6.QtCore import QModelIndex, Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QMenu,
    QTableView,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from src.data.settings.AppSettings import AppSettings
from src.models.Projects import ProjectsModel


class EditTransactionsToolBar(QToolBar):

    def __init__(self, projects_model: "ProjectsModel", parent=None):
        super(EditTransactionsToolBar, self).__init__(parent)

        self._projects_model = projects_model

        self.setMovable(True)

        # Add Transaction Action
        add_transaction_action = QAction("Add Transaction", self)
        add_transaction_action.setStatusTip("Adds a new 'income' transaction")
        add_transaction_action.triggered.connect(self._add_transaction)
        self.addAction(add_transaction_action)

    def _add_transaction(self) -> None:
        pass


class TransactionsTableView(QTableView):

    def __init__(self, parent):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)

    def open_context_menu(self, position):
        """
        Custom context menu that opens at right-click
        """
        index = self.indexAt(position)  # type: QModelIndex

        if index.isValid():
            pass


class EditTransactionsPage(QWidget):
    def __init__(
        self, projects_model: "ProjectsModel", settings: "AppSettings", parent=None
    ):
        super(EditTransactionsPage, self).__init__(parent=parent)

        self._projects_model = projects_model
        self._settings = settings

        self._setup_ui()
        self._set_models()
        self._setup_connections()

    def _setup_ui(self) -> None:
        self._layout = QVBoxLayout(self)

        self._view = TransactionsTableView(self)
        self._view.setAlternatingRowColors(True)
        self._view.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        self._header_view = QHeaderView(Qt.Orientation.Horizontal, self._view)
        self._header_view.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self._header_view.setStretchLastSection(True)
        self._view.setHorizontalHeader(self._header_view)

        self._layout.addWidget(self._view)

    def _set_models(self) -> None:
        pass

    def _setup_connections(self) -> None:
        pass
