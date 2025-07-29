from threading import main_thread
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
from src.models.Transactions import TransactionsOverviewTableModel
from src.ui.ManageBankAccounts import ManageBankAccountsDialog
from src.ui.ManageCounterParts import ManageCounterPartsDialog
from src.ui.delegates.DateDelegate import DateDelegate
from src.ui.transactions.ManageCategories import CategoriesDialog
from src.ui.transactions.ManageTransactionCSVReaders import ReadersDialog

if TYPE_CHECKING:
    from src.ui.MainWindow import MainWindow
from src.ui.delegates.ComboBoxDelegate import ComboBoxDelegate
from typing import Optional


class EditTransactionsToolBar(QToolBar):

    def __init__(self, projects_model: "ProjectsModel",
                 settings: AppSettings,
                 parent: "MainWindow"):
        super(EditTransactionsToolBar, self).__init__(parent)

        self._main_window = parent
        self._projects_model = projects_model
        self._transactions_model = self._projects_model.transactions_model  # type: TransactionsOverviewTableModel
        self._settings = settings

        self.setMovable(True)

        # Add Transaction Action
        add_transaction_action = QAction("Add Transaction", self)
        add_transaction_action.setStatusTip("Adds a new 'transactions' transaction")
        add_transaction_action.triggered.connect(self._add_transaction)
        self.addAction(add_transaction_action)

        # Manage Income Categories Action
        manage_categories_action = QAction("Manage Categories", self)
        manage_categories_action.triggered.connect(self._open_manage_categories_dialog)
        self.addAction(manage_categories_action)

        # Manage Counterparts Action
        manage_counterparts_action = QAction("Manage Counterparts", self)
        manage_counterparts_action.triggered.connect(self._open_manage_counterparts_dialog)
        self.addAction(manage_counterparts_action)

        # Manage Bank Accounts Action
        manage_accounts_action = QAction("Manage Accounts", self)
        manage_accounts_action.triggered.connect(self._open_manage_bank_accounts_dialog)
        self.addAction(manage_accounts_action)

        # Manage Readers Action
        manage_readers_action = QAction("Manage .csv Readers", self)
        manage_readers_action.triggered.connect(self._open_manage_readers_dialog)
        self.addAction(manage_readers_action)

    def set_transactions_model(self, transactions_model: TransactionsOverviewTableModel) -> None:
        self._transactions_model = transactions_model

    def _add_transaction(self) -> None:
        self._transactions_model.create_new_item()

    def _open_manage_categories_dialog(self) -> None:
        dialog = CategoriesDialog(projects_model=self._projects_model, settings=self._settings, parent=self)
        self._center_dialog(dialog)
        dialog.exec()

    def _open_manage_counterparts_dialog(self) -> None:
        dialog = ManageCounterPartsDialog(projects_model=self._projects_model,
                                          settings=self._settings,
                                          parent=self)

        self._center_dialog(dialog)
        dialog.exec()

    def _open_manage_bank_accounts_dialog(self) -> None:
        dialog = ManageBankAccountsDialog(projects_model=self._projects_model,
                                          settings=self._settings,
                                          parent=self)

        self._center_dialog(dialog)
        dialog.exec()

    def _open_manage_readers_dialog(self) -> None:
        dialog = ReadersDialog(projects_model=self._projects_model, settings=self._settings, parent=self)
        self._center_dialog(dialog)
        dialog.exec()

    def _center_dialog(self, dialog: QDialog):
        """Centers a dialog with respect to the main window."""

        # Calculate the center position
        main_window_rect = self._main_window.geometry()
        dialog_size = dialog.sizeHint() # Get the preferred size of the dialog

        # Calculate the top-left corner for the dialog to be centered
        x = main_window_rect.x() + (main_window_rect.width() - dialog_size.width()) // 2
        y = main_window_rect.y() + (main_window_rect.height() - dialog_size.height()) // 2

        dialog.move(x, y)


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
        self, projects_model: "ProjectsModel", settings: "AppSettings", parent:"MainWindow",
    ):
        super(EditTransactionsPage, self).__init__(parent=parent)

        self._projects_model = projects_model
        self._settings = settings
        self._main_window = parent

        self._setup_ui()
        self._set_models()
        self._setup_connections()

    def _setup_ui(self) -> None:
        self._layout = QVBoxLayout(self)

        self._view = TransactionsTableView(self)
        self._view.setAlternatingRowColors(True)
        self._view.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        self._view.setItemDelegateForColumn(TransactionsOverviewTableModel.cols.DATE, DateDelegate(settings=self._settings, parent=self._view))
        for column in TransactionsOverviewTableModel.comboBox_columns:
            self._view.setItemDelegateForColumn(column, ComboBoxDelegate(self._view))

        self._header_view = QHeaderView(Qt.Orientation.Horizontal, self._view)
        self._header_view.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self._header_view.setStretchLastSection(True)
        self._view.setHorizontalHeader(self._header_view)

        self._layout.addWidget(self._view)

    def _set_models(self) -> None:
        transactions_model = self._projects_model.transactions_model

        self._view.setModel(transactions_model)
        self._header_view.setModel(transactions_model)

    def _setup_connections(self) -> None:
        pass
