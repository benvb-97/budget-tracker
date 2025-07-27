import json
from enum import StrEnum
from os.path import isfile
from typing import TYPE_CHECKING, Any, ItemsView, KeysView, ValuesView

from src.data.settings.SettingTypes import Setting
from src.paths import APP_SETTINGS_FILEPATH

if TYPE_CHECKING:
    from src.data.settings.AppSettings import AppSettings


class SettingsSubGroup:
    group_key = None  # type: str
    subgroup_key = None  # type: str
    text = ""  # type: str

    def __init__(self, app_settings: "AppSettings") -> None:
        self._app_settings = app_settings

        self._settings = {}  # type: dict[str, Setting]
        self._init_settings()
        self._load_settings_json()

    def __getitem__(self, key: str) -> Setting:
        return self._settings[key]

    def keys(self) -> KeysView[str]:
        return self._settings.keys()

    def values(self) -> ValuesView[Setting]:
        return self._settings.values()

    def items(self) -> ItemsView[str, Setting]:
        return self._settings.items()

    def _init_settings(self) -> None:
        raise NotImplementedError

    def _load_settings_json(self) -> None:
        if not isfile(APP_SETTINGS_FILEPATH):
            return

        with open(file=APP_SETTINGS_FILEPATH, mode="r") as read_file:
            json_dict = json.load(read_file)

        if self.group_key not in json_dict:
            return
        json_dict = json_dict[self.group_key]
        if self.subgroup_key not in json_dict:
            return
        json_dict = json_dict[self.subgroup_key]

        for key, setting in self._settings.items():
            setting.value = json_dict[key] if key in json_dict else setting.value

    def json_dict(self) -> dict[str, Any]:
        json_dict = {key: setting.value for key, setting in self._settings.items()}
        return json_dict


class SettingsGroup:
    group_key = None  # type: str
    text = ""

    def __init__(self, app_settings: "AppSettings") -> None:
        self._app_settings = app_settings

        self._settings = (
            {}
        )  # type: dict[str, Setting]  # Combines settings from all sub-groups
        self._setting_subgroups = {}  # type: dict[str, SettingsSubGroup]
        self._init_setting_subgroups()

        for subgroup in self._setting_subgroups.values():
            for key, setting in subgroup.items():
                self._settings[key] = setting

    def __getitem__(self, key: str) -> Setting:
        return self._settings[key]

    def keys(self) -> KeysView[str]:
        return self._setting_subgroups.keys()

    def values(self) -> ValuesView[SettingsSubGroup]:
        return self._setting_subgroups.values()

    def items(self) -> ItemsView[str, SettingsSubGroup]:
        return self._setting_subgroups.items()

    def _init_setting_subgroups(self) -> None:
        raise NotImplementedError

    def json_dict(self) -> dict[str, Any]:
        json_dict = {
            key: settings_subgroup.json_dict()
            for key, settings_subgroup in self._setting_subgroups.items()
        }
        return json_dict


class SettingGroups(StrEnum):
    GENERAL = "GENERAL"
