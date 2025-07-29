import ctypes
import logging
import logging.config
import sys
from typing import Optional

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication

from src.data.settings.AppSettings import AppSettings
from src.data.settings.GeneralSettings import GeneralSettingKeys
from src.models.Projects import ProjectsModel
from src.utils.logging_config import setup_logging
from src.data.Projects import Projects
from src.ui.MainWindow import MainWindow


class MainBackend(QObject):
    def __init__(
        self,
        application: Optional[QApplication],
        settings: AppSettings,
    ) -> None:
        super().__init__()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(settings.general[GeneralSettingKeys.DEBUG_LEVEL].value)

        self._application = application
        self._settings = settings
        self._init_models()

        # Init main window
        self._main_window = MainWindow(projects_model=self._projects_model, settings=self._settings)
        self._main_window.show()

    def _init_models(self) -> None:
        """
        Initializes the overarching data structures
        - projects stores all project related data per project
        :return:
        """
        self.projects = Projects(settings=self._settings)
        self._projects_model = ProjectsModel(projects=self.projects, settings=self._settings, parent=self)


def main() -> None:
    # Initialize logger
    setup_logging()

    # Initialize settings
    settings = AppSettings()

    # Init application and set style
    app = QApplication(sys.argv)
    app.setStyle(settings.general[GeneralSettingKeys.APPLICATION_STYLE].value)

    backend = MainBackend(application=app, settings=settings)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
