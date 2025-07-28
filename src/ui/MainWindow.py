from optparse import Option
from typing import Optional

from PySide6.QtWidgets import QMainWindow, QMenuBar, QSplitter, QToolBar, QWidget

from src.data.settings.AppSettings import AppSettings
from src.models.Projects import ProjectsModel
from src.ui.menus.ExpensesMenu import ExpensesMenu
from src.ui.menus.FileMenu import FileMenu
from src.ui.SideBar import SideBar
from src.ui.WelcomePage import WelcomePage
from src.ui.menus.IncomeMenu import IncomeMenu
from src.ui.menus.MainMenuBar import MainMenuBar


class MainWindow(QMainWindow):
    def __init__(self, projects_model: ProjectsModel, settings: AppSettings) -> None:
        super(MainWindow, self).__init__()

        self._projects_model = projects_model
        self._settings = settings
        self._tool_bar = None  # type: Optional[QToolBar]
        self._current_page = None  # type: Optional[QWidget]

        self._setup_ui()

        self.showMaximized()

    def _setup_ui(self) -> None:
        self.setWindowTitle("Budget Planner")

        self._create_central_widget()
        self._create_menu_bar()

    def _create_central_widget(self):
        """Creates a placeholder widget for the main window."""

        self._main_splitter = QSplitter(self)
        self.setCentralWidget(self._main_splitter)

        self._projects_view = SideBar(projects_model=self._projects_model, parent=self)

        self._main_splitter.addWidget(self._projects_view)
        self.set_current_page(new_page=WelcomePage(self))

    def _create_menu_bar(self):
        """Creates the menu bar and adds menus."""
        self._menu_bar = MainMenuBar(projects_model=self._projects_model, settings=self._settings, parent=self)
        self.setMenuBar(self._menu_bar)

    def _remove_current_tool_bar(self):
        if self._tool_bar is not None:
            self.removeToolBar(self._tool_bar)
            self._tool_bar.setParent(None)
            self._tool_bar = None

    def set_current_tool_bar(self, new_tool_bar: QToolBar = None) -> None:
        self._remove_current_tool_bar()

        self._tool_bar = new_tool_bar
        if self._tool_bar is not None:
            self.addToolBar(new_tool_bar)

    def set_current_page(self, new_page: QWidget) -> None:
        self._current_page = new_page

        if self._main_splitter.count() < 2:
            self._main_splitter.addWidget(new_page)
        else:
            self._main_splitter.replaceWidget(1, new_page)

