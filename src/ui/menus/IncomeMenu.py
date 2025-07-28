
from PySide6.QtWidgets import QMenu, QDialog, QFileDialog
from PySide6.QtGui import QAction
from typing import TYPE_CHECKING

from src.data.settings.AppSettings import AppSettings
from src.models.Projects import ProjectsModel
from src.ui.income.EditTransactions import EditTransactionsToolBar, EditTransactionsPage

if TYPE_CHECKING:
    from src.ui.MainWindow import MainWindow


class IncomeMenu(QMenu):

    def __init__(self, projects_model: ProjectsModel, settings: AppSettings, parent: "MainWindow") -> None:
        super().__init__(title="Income", parent=parent)

        self._projects_model = projects_model
        self._settings = settings
        self._main_window = parent

        # Edit Income Data Action
        edit_transactions_action = QAction("Edit Transactions", self)
        edit_transactions_action.setStatusTip("Edit income transactions")
        edit_transactions_action.triggered.connect(self._navigate_to_edit_transactions_page)
        self.addAction(edit_transactions_action)

    def _navigate_to_edit_transactions_page(self) -> None:
        tool_bar = EditTransactionsToolBar(projects_model=self._projects_model, settings=self._settings, parent=self._main_window)
        self._main_window.set_current_tool_bar(tool_bar)

        edit_transactions_page = EditTransactionsPage(projects_model=self._projects_model,
                                                      settings=self._settings,
                                                      parent=self._main_window,
                                                      )
        self._main_window.set_current_page(edit_transactions_page)