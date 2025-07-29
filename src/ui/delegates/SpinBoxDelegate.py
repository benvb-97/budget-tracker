from PySide6.QtCore import (
    QSortFilterProxyModel,
    Qt,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox, QSpinBox,
    QStyledItemDelegate,
)


# This delegate will provide a QSpinBox for editing integer data.
class SpinBoxDelegate(QStyledItemDelegate):
    def __init__(self, lbound: int, ubound: int, parent=None):
        """

        :param lbound: lower bound of the spinBox
        :param ubound: upper bound of the spinBox
        :param parent:
        """
        self._lbound = lbound
        self._ubound = ubound

        super().__init__(parent)

    def createEditor(self, parent, option, index):
        # Creates and returns a QSpinBox widget to be used as an editor.
        # The parent is the QTableView's viewport.
        editor = QSpinBox(parent)
        # Set a reasonable range for the spin box. Adjust as needed.
        editor.setRange(self._lbound, self._ubound)
        editor.setSingleStep(1)
        return editor

    def setEditorData(self, editor, index):
        # Populates the editor (QSpinBox) with data from the model.
        # The data is retrieved using Qt.EditRole.
        value = index.model().data(index, Qt.EditRole)
        if value is not None:
            # Ensure the value is an integer before setting it.
            try:
                editor.setValue(int(value))
            except ValueError:
                editor.setValue(0) # Default to 0 if conversion fails
        else:
            editor.setValue(0) # Default to 0 if no value

    def setModelData(self, editor, model, index):
        # Writes the data from the editor (QSpinBox) back to the model.
        # The value is retrieved from the QSpinBox.
        editor.interpretText() # Ensures the spinbox's value is updated from its text
        value = editor.value()
        # Set the data in the model using Qt.EditRole.
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        # Sets the geometry (position and size) of the editor.
        # The editor should occupy the rectangle of the cell.
        editor.setGeometry(option.rect)