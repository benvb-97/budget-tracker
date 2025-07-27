
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.ui.MainWindow import MainWindow


class FileMenu(QMenu):


    def __init__(self, parent: "MainWindow") -> None:
        super().__init__(title="File", parent=parent)

        self._main_window = parent

        # Settings Action
        settings_action = QAction("&Settings", self)
        settings_action.setStatusTip("Open application settings")
        settings_action.triggered.connect(self._main_window.open_settings_dialog)
        self.addAction(settings_action)

        # Add a separator line
        self.addSeparator()

        # Quit Action
        quit_action = QAction("&Quit", self)
        quit_action.setStatusTip("Exit the application")
        quit_action.triggered.connect(self._main_window.close)  # Connects to the window's close method

        self.addAction(quit_action)
