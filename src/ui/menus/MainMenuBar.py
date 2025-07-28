from PySide6.QtWidgets import QMenuBar

from src.data.settings.AppSettings import AppSettings
from src.models.Projects import ProjectsModel
from typing import TYPE_CHECKING

from src.ui.menus.ExpensesMenu import ExpensesMenu
from src.ui.menus.FileMenu import FileMenu
from src.ui.menus.IncomeMenu import IncomeMenu

if TYPE_CHECKING:
    from src.ui.MainWindow import MainWindow


class MainMenuBar(QMenuBar):

    def __init__(self, projects_model: ProjectsModel, settings: AppSettings, parent: "MainWindow") -> None:
        super().__init__(parent)

        self._main_window = parent
        self._projects_model = projects_model
        self._settings = settings

        self._create_menus()
        self._projects_model.current_project_changed.connect(self._toggle_menus)
        self._toggle_menus()

    def _create_menus(self) -> None:
        self._file_menu = FileMenu(projects_model=self._projects_model, settings=self._settings, parent=self._main_window)
        self._income_menu = IncomeMenu(projects_model=self._projects_model, settings=self._settings, parent=self._main_window)
        self._expenses_menu = ExpensesMenu(projects_model=self._projects_model, settings=self._settings, parent=self._main_window)

        self.addMenu(self._file_menu)
        self.addMenu(self._income_menu)
        self.addMenu(self._expenses_menu)

    def _toggle_menus(self) -> None:
        if self._projects_model.has_project_opened:
            self._income_menu.setEnabled(True)
            self._expenses_menu.setEnabled(True)
        else:
            self._income_menu.setEnabled(False)
            self._expenses_menu.setEnabled(False)

