from PySide6.QtWidgets import (QStyledItemDelegate, QDateEdit, QVBoxLayout, QWidget, QStyleOptionViewItem)
from PySide6.QtCore import Qt, QModelIndex, QDate
from PySide6.QtGui import QPainter
from src.data.settings.AppSettings import AppSettings
from src.data.settings.GeneralSettings import GeneralSettingKeys


class DateDelegate(QStyledItemDelegate):
    def __init__(self, settings: AppSettings, parent=None):
        super().__init__(parent)

        self._settings = settings

    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setCalendarPopup(True) # This is crucial for the calendar popup

        date_format = self._settings.general[GeneralSettingKeys.DATE_FORMAT].value
        editor.setDisplayFormat(date_format) # Set desired display format
        return editor

    def setEditorData(self, editor: QDateEdit, index):
        model_data = index.model().data(index, Qt.ItemDataRole.EditRole)

        if model_data is None:
            pass
        elif isinstance(model_data, QDate):
            editor.setDate(model_data)
        else:
            raise TypeError(f"DateDelegate requires a QDate instance to set the date. Passed {model_data}")

    def setModelData(self, editor: QDateEdit, model, index):
        if index.column() == 1:
            new_date = editor.date() # QDate object from the editor
            model.setData(index, new_date, Qt.ItemDataRole.EditRole)
        else:
            super().setModelData(editor, model, index)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        """
        Paints the item's content when the editor is not active. Reimplement in order to show correct date format.
        """
        model_data = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        date_format = self._settings.general[GeneralSettingKeys.DATE_FORMAT].value

        if isinstance(model_data, QDate):
            # Format the QDate for display
            text = model_data.toString(date_format)
        else:
            text = ""

        # Now, draw our custom formatted text directly
        painter.save()
        # Draw the text within the item's rectangle
        painter.drawText(option.rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)
        painter.restore()

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)