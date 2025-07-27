
from PySide6.QtWidgets import QMenu, QDialog
from PySide6.QtGui import QAction
from typing import TYPE_CHECKING

from src.data.settings.AppSettings import AppSettings
from src.ui.settings.SettingsDialog import SettingsDialog

if TYPE_CHECKING:
    from src.ui.MainWindow import MainWindow


class FileMenu(QMenu):


    def __init__(self, settings: AppSettings, parent: "MainWindow") -> None:
        super().__init__(title="File", parent=parent)

        self._settings = settings
        self._main_window = parent

        # New Project Action
        new_project_action = QAction("New Project", self)
        new_project_action.setStatusTip("Create a new project")
        new_project_action.triggered.connect(self._create_new_project)
        self.addAction(new_project_action)

        # Open Project Action
        open_project_action = QAction("Open Project", self)
        open_project_action.setStatusTip("Open an existing project")
        open_project_action.triggered.connect(self._open_project)
        self.addAction(open_project_action)

        # Add separator
        self.addSeparator()

        # Save Current Project Action
        save_current_project_action = QAction("Save Current Project", self)
        save_current_project_action.setStatusTip("Saves the active project")
        save_current_project_action.triggered.connect(self._save_current_project)
        self.addAction(save_current_project_action)

        # Save As Action
        save_as_action = QAction("Save As", self)
        save_as_action.setStatusTip("Saves the active project with a new directory name")
        save_as_action.triggered.connect(self._save_as)
        self.addAction(save_as_action)

        # Save All Action
        save_all_action = QAction("Save All", self)
        save_all_action.setStatusTip("Saves all opened projects")
        save_all_action.triggered.connect(self._save_all)
        self.addAction(save_all_action)

        # Add separator
        self.addSeparator()

        # Close Current Project Action
        close_current_project_action = QAction("Close Current Project", self)
        close_current_project_action.setStatusTip("Closes the active project without saving")
        close_current_project_action.triggered.connect(self._close_current_project)
        self.addAction(close_current_project_action)

        # Close All Projects Action
        close_all_projects_action = QAction("Close All Projects", self)
        close_all_projects_action.setStatusTip("Closes all opened projects without saving")
        close_all_projects_action.triggered.connect(self._close_all_projects)
        self.addAction(close_all_projects_action)

        # Add separator
        self.addSeparator()

        # Settings Action
        settings_action = QAction("Settings", self)
        settings_action.setStatusTip("Open application settings")
        settings_action.triggered.connect(self.open_settings_dialog)
        self.addAction(settings_action)

        # Add separator
        self.addSeparator()

        # Quit Action
        quit_action = QAction("Quit", self)
        quit_action.setStatusTip("Exit the application")
        quit_action.triggered.connect(self._main_window.close)  # Connects to the window's close method

        self.addAction(quit_action)

    def _create_new_project(self):
        pass

    def _open_project(self):
        pass

    def _save_current_project(self):
        pass

    def _save_as(self):
        pass

    def _save_all(self):
        pass

    def _close_current_project(self):
        pass

    def _close_all_projects(self):
        pass

    def open_settings_dialog(self) -> None:
        dialog = SettingsDialog(self, settings=self._settings)
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