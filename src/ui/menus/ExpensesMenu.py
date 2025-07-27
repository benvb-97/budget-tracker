
from PySide6.QtWidgets import QMenu, QDialog, QFileDialog
from PySide6.QtGui import QAction
from typing import TYPE_CHECKING

from src.data.settings.AppSettings import AppSettings
from src.models.Projects import ProjectsModel
from src.ui.expenses.EditTransactions import EditTransactionsToolBar, EditTransactionsPage

if TYPE_CHECKING:
    from src.ui.MainWindow import MainWindow


class ExpensesMenu(QMenu):

    def __init__(self, projects_model: ProjectsModel, settings: AppSettings, parent: "MainWindow") -> None:
        super().__init__(title="Expenses", parent=parent)

        self._projects_model = projects_model
        self._settings = settings
        self._main_window = parent

        # Edit Income Data Action
        edit_transactions_page = QAction("Edit Transactions", self)
        edit_transactions_page.setStatusTip("Edit expense transactions")
        edit_transactions_page.triggered.connect(self._navigate_to_edit_transactions_page)
        self.addAction(edit_transactions_page)

    def _navigate_to_edit_transactions_page(self) -> None:
        tool_bar = EditTransactionsToolBar(projects_model=self._projects_model, parent=self._main_window)
        self._main_window.set_current_tool_bar(tool_bar)

        edit_transactions_page = EditTransactionsPage(projects_model=self._projects_model,
                                                      settings=self._settings,
                                                      parent=self._main_window,
                                                      )
        self._main_window.set_current_page(edit_transactions_page)