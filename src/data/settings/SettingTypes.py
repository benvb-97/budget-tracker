from typing import TypeAlias


class SettingTypes:

    INT = 0
    FLOAT = 1
    STR = 2
    FILEPATH = 3
    BOOL = 4
    COMBO_BOX = 5
    COLOR = 6
    DIRECTORY = 7


class IntSetting:

    setting_type = SettingTypes.INT

    def __init__(self, key: str, text: str, _min: int, _max: int, default: int) -> None:
        self.key = key
        self.text = text
        self.min = _min
        self.max = _max

        self.value = default


class FloatSetting:

    setting_type = SettingTypes.FLOAT

    def __init__(
        self, key: str, text: str, _min: float, _max: float, default: float
    ) -> None:
        self.key = key
        self.text = text
        self.min = _min
        self.max = _max

        self.value = default


class StrSetting:

    setting_type = SettingTypes.STR

    def __init__(self, key: str, text: str, default: str) -> None:
        self.key = key
        self.text = text
        self.value = default


class FilepathSetting:

    setting_type = SettingTypes.FILEPATH

    def __init__(
        self, key: str, text: str, dialog_caption: str, dialog_filter: str, default: str
    ) -> None:
        self.key = key
        self.text = text
        self.dialog_caption = dialog_caption
        self.dialog_filter = dialog_filter

        self.value = default


class DirectorySetting:

    setting_type = SettingTypes.DIRECTORY

    def __init__(self, key: str, text: str, dialog_caption: str, default: str) -> None:
        self.key = key
        self.text = text
        self.dialog_caption = dialog_caption
        # self.dialog_filter = dialog_filter

        self.value = default


class BoolSetting:

    setting_type = SettingTypes.BOOL

    def __init__(self, key: str, text: str, default: bool) -> None:
        self.key = key
        self.text = text

        self.value = default


class ComboBoxSetting:
    setting_type = SettingTypes.COMBO_BOX

    def __init__(
        self, key: str, text: str, choices: dict[str, str], default: str
    ) -> None:
        self.key = key
        self.text = text
        self.choices = choices

        self.value = default


class ColorSetting:
    setting_type = SettingTypes.COLOR

    def __init__(self, key: str, text: str, default: tuple[int, int, int, int]) -> None:
        self.key = key
        self.text = text
        self.value = default

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        return self.value


Setting: TypeAlias = (
    IntSetting
    | FloatSetting
    | StrSetting
    | FilepathSetting
    | BoolSetting
    | ComboBoxSetting
    | ColorSetting
)
