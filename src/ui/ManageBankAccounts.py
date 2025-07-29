from typing import TYPE_CHECKING

from PySide6.QtCore import QItemSelectionModel, QModelIndex, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHeaderView,
    QListView,
    QMenu,
    QPushButton,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.data.settings.AppSettings import AppSettings
from src.models.BankAccounts import BankAccountsOverviewListModel, BankAccountDataModel
from src.models.Projects import ProjectsModel


class BankAccountsListView(QListView):
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
            model: BankAccountsOverviewListModel = index.model()

            menu = QMenu(self)

            # Add actions to the context menu
            delete_action = QAction("Delete bank account", self)
            delete_action.triggered.connect(lambda: model.delete_item(index))
            menu.addAction(delete_action)

            # Show the menu at the cursor position
            menu.exec(self.viewport().mapToGlobal(position))


class ManageBankAccountsDialog(QDialog):
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
        self.setWindowTitle("Manage Bank Accounts")

        self._layout = QVBoxLayout(self)
        self._splitter = QSplitter(self)
        self._layout.addWidget(self._splitter)

        # 1. Left part of splitter: list of bank accounts and button to create more
        self._accounts_view = BankAccountsListView(self)
        self._accounts_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems
        )
        self._accounts_view.setHorizontalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )

        self._new_account_button = QPushButton("New Bank Account", self)

        accounts_widget = QWidget(self)
        accounts_layout = QVBoxLayout(accounts_widget)
        accounts_layout.addWidget(self._accounts_view)
        accounts_layout.addStretch()
        accounts_layout.addWidget(self._new_account_button)
        self._splitter.addWidget(accounts_widget)

        # Right part of splitter: list of values within set and button to create more
        self._account_view = QTableView(self)

        self._account_header_view = QHeaderView(
            Qt.Orientation.Vertical, self._account_view
        )
        self._account_header_view.setDefaultAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Align header text center
        self._account_view.setVerticalHeader(self._account_header_view)
        self._account_view.horizontalHeader().setStretchLastSection(True)
        self._account_view.horizontalHeader().hide()

        account_widget = QWidget(self)
        account_layout = QVBoxLayout(account_widget)
        account_layout.addWidget(self._account_view)
        account_layout.addStretch()
        self._splitter.addWidget(account_widget)

    def _set_models(self) -> None:
        self._accounts_model = self._projects_model.bank_accounts_model
        self._account_model = BankAccountDataModel(accounts_model=self._accounts_model, settings=self._settings, parent=self)

        self._account_selection_model = QItemSelectionModel(self._accounts_model)

        self._accounts_view.setModel(self._accounts_model)
        self._accounts_view.setSelectionModel(self._account_selection_model)

        self._account_view.setModel(self._account_model)
        self._account_header_view.setModel(self._account_model)

    def _setup_connections(self) -> None:
        self._account_selection_model.selectionChanged.connect(
            self._accounts_model.change_selection
        )
        self._new_account_button.clicked.connect(self._accounts_model.create_new_item)
