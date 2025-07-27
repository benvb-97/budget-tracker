from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.ui.settings.SettingsTab import SettingsTab
from src.data.settings.AppSettings import AppSettings
from src.data.settings.SettingsGroups import SettingsGroup


class SettingsDialog(QDialog):

    def __init__(self, parent, settings: AppSettings):
        super().__init__(parent=parent)
        self._settings = settings

        self._setup_ui()
        self._set_models()
        self._setup_connections()

    def _setup_ui(self) -> None:
        self.setWindowTitle("Settings")

        self._layout = QHBoxLayout(self)
        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Orientation.Horizontal)
        self._layout.addWidget(splitter)

        # Left
        self._list_widget = QListWidget(self)
        splitter.addWidget(self._list_widget)

        # Right
        right_container = QWidget(self)
        right_layout = QVBoxLayout(right_container)
        splitter.addWidget(right_container)

        # Setting group pages
        self._settings_pages = [
            SettingsPage(self, group) for group in self._settings.setting_groups
        ]
        self._stacked_widget = QStackedWidget(self)
        for page in self._settings_pages:
            self._stacked_widget.addWidget(page)
        right_layout.addWidget(self._stacked_widget)

        # Buttons
        buttons_widget = QWidget(self)
        buttons_layout = QHBoxLayout(buttons_widget)

        self._ok_button = QPushButton("OK")
        self._cancel_button = QPushButton("Cancel")
        self._apply_button = QPushButton("Apply")

        buttons_layout.addStretch()
        buttons_layout.addWidget(self._ok_button)
        buttons_layout.addWidget(self._cancel_button)
        buttons_layout.addWidget(self._apply_button)

        right_layout.addStretch()
        right_layout.addWidget(buttons_widget)

    def _set_models(self) -> None:
        for group in self._settings.setting_groups:
            self._list_widget.addItem(group.text)

    def _setup_connections(self) -> None:
        self._list_widget.currentRowChanged.connect(
            self._stacked_widget.setCurrentIndex
        )
        self._ok_button.clicked.connect(self.accept)
        self._cancel_button.clicked.connect(self.reject)
        self._apply_button.clicked.connect(self._save_settings)

    def _save_settings(self) -> None:
        for page in self._settings_pages:
            page.read_settings_from_ui()
        self._settings.save_settings()

    def accept(self) -> None:
        self._save_settings()
        super().accept()


class SettingsPage(QWidget):
    def __init__(self, parent, settings: SettingsGroup):
        super().__init__(parent=parent)
        self._settings = settings

        self._setting_tabs = {}  # type: dict[str, SettingsTab]
        self._setup_ui()

    def _setup_ui(self) -> None:
        self._layout = QVBoxLayout(self)

        # Setting group tabs
        self._tab_widget = QTabWidget(self)
        self._layout.addWidget(self._tab_widget)

        for key, subgroup_settings in self._settings.items():
            widget = SettingsTab(self, subgroup_settings=subgroup_settings)
            self._tab_widget.addTab(widget, subgroup_settings.text)
            self._setting_tabs[key] = widget

    def read_settings_from_ui(self) -> None:
        for tab in self._setting_tabs.values():
            tab.read_settings_from_ui()
