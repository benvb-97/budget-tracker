import ctypes
import logging
import logging.config
import sys
from typing import Optional

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from src.utils.logging_config import setup_logging
import os
from src.ui.MainWindow import MainWindow


class MainBackend(QObject):
    def __init__(
        self,
        application: Optional[QApplication],
    ) -> None:
        super().__init__()

        self.logger = logging.getLogger(__name__)
        self._application = application

        # Init main window
        self._main_window = MainWindow()
        self._main_window.show()


def main() -> None:
    # Initialize logger
    setup_logging()

    # Init application
    app = QApplication(sys.argv)

    backend = MainBackend(application=app)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
