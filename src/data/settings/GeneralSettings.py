from enum import StrEnum
from typing import TYPE_CHECKING

from src.data.Currencies import Currencies
from src.data.settings.SettingsGroups import SettingGroups, SettingsGroup, SettingsSubGroup
from src.data.settings.SettingTypes import BoolSetting, ComboBoxSetting, IntSetting

if TYPE_CHECKING:
    from src.data.settings.AppSettings import AppSettings

from src.data.settings.ComboBoxChoices import (
    ApplicationStyles,
    DebugLevels,
    application_styles,
    debug_levels, currencies,
)


class GeneralSubGroups(StrEnum):
    DEBUG = "debug"
    STYLE = "style"


class GeneralSettings(SettingsGroup):
    group_key = SettingGroups.GENERAL
    text = "General"

    def _init_setting_subgroups(self) -> None:
        self._setting_subgroups = {
            GeneralSubGroups.DEBUG: DebugSettings(self._app_settings),
            GeneralSubGroups.STYLE: StyleSettings(self._app_settings),
        }


class DebugSettings(SettingsSubGroup):
    group_key = SettingGroups.GENERAL
    subgroup_key = GeneralSubGroups.DEBUG
    text = "Debugging"

    def _init_settings(self) -> None:
        settings = [
            ComboBoxSetting(
                key=GeneralSettingKeys.DEBUG_LEVEL,
                text="Debug level",
                choices=debug_levels,
                default=DebugLevels.DEBUG,
            ),
        ]
        self._settings = {setting.key: setting for setting in settings}


class StyleSettings(SettingsSubGroup):
    group_key = SettingGroups.GENERAL
    subgroup_key = GeneralSubGroups.STYLE
    text = "Style"

    def _init_settings(self) -> None:
        settings = [
            ComboBoxSetting(
                key=GeneralSettingKeys.APPLICATION_STYLE,
                text="Application Style (RESTART)",
                choices=application_styles,
                default=ApplicationStyles.FUSION,
            ),
            ComboBoxSetting(
                key=GeneralSettingKeys.CURRENCY,
                text="Currency",
                choices=currencies,
                default=Currencies.EUR,
            )
        ]
        self._settings = {setting.key: setting for setting in settings}


class GeneralSettingKeys(StrEnum):
    DEBUG_LEVEL = "debug_level"
    APPLICATION_STYLE = "application_style"
    CURRENCY="currency"
