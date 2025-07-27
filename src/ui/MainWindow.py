from PySide6.QtWidgets import QMainWindow, QMenuBar, QSplitter

from src.data.settings.AppSettings import AppSettings
from src.models.Projects import ProjectsModel
from src.ui.menus.FileMenu import FileMenu
from src.ui.SideBar import SideBar
from src.ui.WelcomePage import WelcomePage


class MainWindow(QMainWindow):
    def __init__(self, projects_model: ProjectsModel, settings: AppSettings) -> None:
        super(MainWindow, self).__init__()

        self._projects_model = projects_model
        self._settings = settings

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

        welcome_page = WelcomePage(self)

        self._main_splitter.addWidget(self._projects_view)
        self._main_splitter.addWidget(welcome_page)

    def _create_menu_bar(self):
        """Creates the menu bar and adds menus."""
        self._menu_bar = QMenuBar(self)
        self.setMenuBar(self._menu_bar)

        self._menu_bar.addMenu(FileMenu(projects_model=self._projects_model, settings=self._settings, parent=self))
