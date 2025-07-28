from PySide6.QtCore import (
    QSortFilterProxyModel,
    Qt,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QStyledItemDelegate,
)


class ComboBoxDelegate(QStyledItemDelegate):
    """
    Provides a delegate that shows a combobox in model views.
    """

    def __init__(self, parent):
        super().__init__(parent)
        # self._editors = {}

    def paint(self, painter, option, index):
        if isinstance(self.parent(), QAbstractItemView):
            self.parent().openPersistentEditor(index)
        super(ComboBoxDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        combo_box = QComboBox(parent)
        combo_box.currentIndexChanged.connect(
            self.commit_editor
        )  # trigger setModelData correctly on index change
        return combo_box

    def commit_editor(self):
        editor = self.sender()
        self.commitData.emit(editor)

    def setEditorData(self, editor: QComboBox, index):
        editor.blockSignals(True)
        editor.clear()

        model = index.model()
        if isinstance(model, QSortFilterProxyModel):
            model = model.sourceModel()
        choices = model.data(index, role=model.comboBoxDataRole)  # type: dict[str, str]

        for userData, text in choices.items():
            editor.addItem(text, userData)
        editor.blockSignals(False)

        value = index.data(Qt.ItemDataRole.DisplayRole)
        num = editor.findData(value)
        editor.setCurrentIndex(num)

    def setModelData(self, editor: QComboBox, model, index):
        value = editor.currentData()
        model.setData(index, value, Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor: QComboBox, option, index):
        editor.setGeometry(option.rect)