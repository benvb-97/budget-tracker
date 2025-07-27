from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class WelcomePage(QWidget):
    def __init__(self, parent) -> None:
        super(WelcomePage, self).__init__(parent=parent)

        self._layout = QVBoxLayout(self)

        title_label = QLabel("Budget Tracker")
        title_label.setFont(QFont("Arial", 80))
        title_label.setMinimumSize(1, 1)

        subtitle_label = QLabel("A tool that helps automate budget tracking")
        subtitle_label.setFont(QFont("Arial", 15))
        subtitle_label.setMinimumSize(1, 1)

        self._layout.addStretch()

        self._layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(subtitle_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self._layout.addStretch()
