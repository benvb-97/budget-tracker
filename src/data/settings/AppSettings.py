import json

from PySide6.QtCore import QObject, Signal
from src.data.settings.GeneralSettings import GeneralSettings
from src.data.settings.SettingsGroups import SettingsGroup, SettingGroups
from src.paths import APP_SETTINGS_FILEPATH


class AppSettings(QObject):

    updated = Signal()  # emitted when settings change

    def __init__(self):
        super().__init__(parent=None)

        self.general = GeneralSettings(self)

    def save_settings(self) -> None:
        json_dict = {
            SettingGroups.GENERAL: self.general.json_dict(),
        }
        with open(file=APP_SETTINGS_FILEPATH, mode="w") as write_file:
            json.dump(json_dict, write_file, indent=4)

        self.updated.emit()

    @property
    def setting_groups(self) -> list[SettingsGroup]:
        return [
            self.general,
        ]
