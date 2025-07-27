import logging
import os.path
from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QDoubleValidator, QIcon, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)
from src.data.settings.SettingsGroups import SettingsSubGroup
from src.data.settings.SettingTypes import Setting, SettingTypes, DirectorySetting, FilepathSetting
from src.paths import IconPaths


class SettingsTab(QWidget):

    def __init__(self, parent, subgroup_settings: SettingsSubGroup):
        super().__init__(parent=parent)
        self._settings = subgroup_settings

        self._setting_objects = (
            {}
        )  # type: dict[str, Union[QSlider, QLineEdit, QCheckBox, QComboBox, QColor, QPushButton]]
        self._pushButton = {}  # type: dict[str, QPushButton]

        self._setup_ui()

    def _setup_ui(self):
        self._layout = QVBoxLayout(self)

        # Option widgets
        setting_type_to_widget_creator_map = {
            SettingTypes.INT: self._create_int_setting_widget,
            SettingTypes.FLOAT: self._create_float_setting_widget,
            SettingTypes.STR: self._create_str_setting_widget,
            SettingTypes.FILEPATH: self._create_filepath_setting_widget,
            SettingTypes.DIRECTORY: self._create_directory_setting_widget,
            SettingTypes.BOOL: self._create_bool_setting_widget,
            SettingTypes.COMBO_BOX: self._create_combo_box_setting_widget,
            SettingTypes.COLOR: self._create_color_setting_widget,
        }
        for key, setting in self._settings.items():
            setting_type_to_widget_creator_map[setting.setting_type](
                key=key, setting=setting
            )

        self._layout.addStretch()

    def _create_int_setting_widget(self, key: str, setting: Setting) -> None:
        widget = QWidget(self)
        layout = QHBoxLayout(widget)

        layout.addWidget(QLabel(setting.text))

        slider = QSlider(widget)
        slider.setRange(setting.min, setting.max)
        slider.setValue(setting.value)
        slider.setOrientation(Qt.Orientation.Horizontal)
        layout.addWidget(slider)

        current_value_label = QLabel(str(setting.value))
        slider.valueChanged.connect(
            lambda value: current_value_label.setText(str(value))
        )
        layout.addWidget(current_value_label)

        self._layout.addWidget(widget)
        self._setting_objects[key] = slider

    def _create_float_setting_widget(self, key: str, setting: Setting) -> None:
        widget = QWidget(self)
        layout = QHBoxLayout(widget)

        layout.addWidget(QLabel(setting.text))

        validator = QDoubleValidator(bottom=setting.min, top=setting.max)
        lineEdit = QLineEdit(widget)
        lineEdit.setValidator(validator)
        lineEdit.setText(f"{setting.value}")
        layout.addWidget(lineEdit)

        self._layout.addWidget(widget)
        self._setting_objects[key] = lineEdit

    def _create_str_setting_widget(self, key: str, setting: Setting) -> None:
        widget = QWidget(self)
        layout = QHBoxLayout(widget)

        layout.addWidget(QLabel(setting.text))

        lineEdit = QLineEdit(widget)
        lineEdit.setText(setting.value)
        layout.addWidget(lineEdit)

        self._layout.addWidget(widget)
        self._setting_objects[key] = lineEdit

    def _create_filepath_setting_widget(self, key: str, setting: Setting) -> None:
        widget = QWidget(self)
        layout = QHBoxLayout(widget)

        layout.addWidget(QLabel(setting.text))

        lineEdit = QLineEdit(setting.value)
        pushButton = QPushButton()
        pushButton.setIcon(QIcon(IconPaths.FOLDER.value))
        pushButton.clicked.connect(
            lambda _, _setting=setting, _lineEdit=lineEdit: self._open_filepath_dialog(
                setting=_setting, lineEdit=_lineEdit
            )
        )

        layout.addWidget(lineEdit)
        layout.addWidget(pushButton)

        self._layout.addWidget(widget)
        self._setting_objects[key] = lineEdit

    def _create_directory_setting_widget(self, key: str, setting: Setting) -> None:
        widget = QWidget(self)
        layout = QHBoxLayout(widget)

        layout.addWidget(QLabel(setting.text))

        lineEdit = QLineEdit(setting.value)
        pushButton = QPushButton()
        pushButton.setIcon(QIcon(IconPaths.FOLDER.value))
        pushButton.clicked.connect(
            lambda _, _setting=setting, _lineEdit=lineEdit: self._open_directory_dialog(
                setting=_setting, lineEdit=_lineEdit
            )
        )

        layout.addWidget(lineEdit)
        layout.addWidget(pushButton)

        self._layout.addWidget(widget)
        self._setting_objects[key] = lineEdit

    def _create_bool_setting_widget(self, key: str, setting: Setting) -> None:
        widget = QWidget(self)
        layout = QHBoxLayout(widget)

        layout.addWidget(QLabel(setting.text))

        checkBox = QCheckBox(widget)
        checkBox.setChecked(setting.value)
        layout.addWidget(checkBox)
        layout.addStretch()

        self._layout.addWidget(widget)
        self._setting_objects[key] = checkBox

    def _create_combo_box_setting_widget(self, key: str, setting: Setting) -> None:
        widget = QWidget(self)
        layout = QHBoxLayout(widget)

        layout.addWidget(QLabel(setting.text))

        comboBox = QComboBox(widget)
        for choice_key, text in setting.choices.items():
            comboBox.addItem(text, choice_key)
        comboBox.setCurrentIndex(comboBox.findData(setting.value))
        layout.addWidget(comboBox)
        layout.addStretch()

        self._layout.addWidget(widget)
        self._setting_objects[key] = comboBox

    def _create_color_setting_widget(self, key: str, setting: Setting) -> None:
        widget = QWidget(self)
        layout = QHBoxLayout(widget)

        layout.addWidget(QLabel(setting.text))

        pushButton = QPushButton("Pick Color")
        self._pushButton[key] = pushButton
        pushButton.clicked.connect(lambda _=None, _key=key: self._pick_color(_key))
        layout.addWidget(pushButton)

        color = QColor()
        color.setRgb(
            setting.value[0], setting.value[1], setting.value[2], setting.value[3]
        )
        pix_map = QPixmap(16, 16)
        pix_map.fill(color)
        pushButton.setIcon(QIcon(pix_map))

        layout.addStretch()
        self._layout.addWidget(widget)
        self._setting_objects[key] = color

    def _open_filepath_dialog(self, setting: FilepathSetting, lineEdit: QLineEdit):
        filename = QFileDialog.getOpenFileName(
            self, caption=setting.dialog_caption, filter=setting.dialog_filter
        )[0]
        if os.path.isfile(filename):
            lineEdit.setText(filename)

    def _open_directory_dialog(self, setting: DirectorySetting, lineEdit: QLineEdit):
        path = QFileDialog.getExistingDirectory(self, caption=setting.dialog_caption)
        if os.path.isdir(path):
            lineEdit.setText(path)
        else:
            logging.getLogger(__name__).debug(f"path: {path} is not a directory.")

    def _pick_color(self, setting_key: str):
        color = QColorDialog.getColor()
        if color.isValid():
            self._setting_objects[setting_key] = color

            pix_map = QPixmap(16, 16)
            pix_map.fill(color)
            self._pushButton[setting_key].setIcon(QIcon(pix_map))

    def read_settings_from_ui(self) -> None:
        for key, setting in self._settings.items():

            if setting.setting_type == SettingTypes.INT:
                setting_object: QSlider = self._setting_objects[key]
                setting.value = setting_object.value()
            elif setting.setting_type == SettingTypes.FLOAT:
                setting_object: QLineEdit = self._setting_objects[key]
                setting.value = float(setting_object.text())
            elif setting.setting_type == SettingTypes.STR:
                setting_object: QLineEdit = self._setting_objects[key]
                setting.value = setting_object.text()
            elif setting.setting_type == SettingTypes.FILEPATH:
                setting_object: QLineEdit = self._setting_objects[key]
                setting.value = setting_object.text()
            elif setting.setting_type == SettingTypes.DIRECTORY:
                setting_object: QLineEdit = self._setting_objects[key]
                setting.value = setting_object.text()
            elif setting.setting_type == SettingTypes.BOOL:
                setting_object: QCheckBox = self._setting_objects[key]
                setting.value = setting_object.isChecked()
            elif setting.setting_type == SettingTypes.COMBO_BOX:
                setting_object: QComboBox = self._setting_objects[key]
                setting.value = setting_object.currentData()
            elif setting.setting_type == SettingTypes.COLOR:
                setting_object: QColor = self._setting_objects[key]
                setting.value = (
                    setting_object.red(),
                    setting_object.green(),
                    setting_object.blue(),
                    setting_object.alpha(),
                )

            else:
                raise NotImplementedError
