from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QMenuBar

from src.data.settings.AppSettings import AppSettings
from src.ui.MainMenus import FileMenu
from src.ui.settings.SettingsDialog import SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self, settings: AppSettings) -> None:
        super(MainWindow, self).__init__()

        self._settings = settings

        self._setup_ui()

        self.showMaximized()

    def _setup_ui(self) -> None:
        self.setWindowTitle("Budget Planner")

        self._create_central_widget()
        self._create_menu_bar()

    def _create_central_widget(self):
        """Creates a placeholder widget for the main window."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        label = QLabel("Welcome to the Main Window!")
        label.setStyleSheet("font-size: 24px; text-align: center;")
        layout.addWidget(label)
        layout.addStretch()

    def _create_menu_bar(self):
        """Creates the menu bar and adds menus."""
        self._menu_bar = QMenuBar(self)
        self.setMenuBar(self._menu_bar)

        self._menu_bar.addMenu(FileMenu(self))

    def open_settings_dialog(self) -> None:
        dialog = SettingsDialog(self, settings=self._settings)
        dialog.exec()
