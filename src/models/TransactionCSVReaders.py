from typing import Optional, TYPE_CHECKING, Any

from src.data.Currencies import Currencies
from src.data.TaggedItems import TaggedItemsType
from src.data.TransactionCategories import TransactionCategory
from src.data.TransactionsCSVReader import TransactionsCSVReader, TransactionCSVColumns
from src.data.settings.AppSettings import AppSettings
from src.data.settings.GeneralSettings import GeneralSettingKeys
from src.models.TaggedItems import TaggedItemsOverviewTableModel, TaggedItemsListModel

if TYPE_CHECKING:
    from src.data.Projects import Project
    from src.models.Projects import ProjectsModel
from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
from enum import IntEnum


class Columns(IntEnum):
    NAME = 0
    DATE_COLUMN = 1
    AMOUNT_COLUMN = 2
    COUNTERPART_COLUMN = 3
    ACCOUNT_COLUMN = 4
    NOTE_COLUMN = 5


class TransactionCSVReadersOverviewModel(TaggedItemsOverviewTableModel):
    cols = Columns

    def __init__(self,
                 projects_model: "ProjectsModel",
                 settings: AppSettings,
                 parent,
                 ) -> None:
        super().__init__(projects_model=projects_model,
                         settings=settings,
                         parent=parent,
                         )

    def _get_project_data(self, project: "Project") -> TaggedItemsType:
        return project.transaction_csv_readers

    def data(self, index=QModelIndex(), role=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None

        reader = self.get_item(index)  # type: TransactionsCSVReader
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if column == self.cols.NAME:
                return reader.name
            elif column == self.cols.DATE_COLUMN:
                return reader.column_map[TransactionCSVColumns.DATE]
            elif column == self.cols.AMOUNT_COLUMN:
                return reader.column_map[TransactionCSVColumns.AMOUNT]
            elif column == self.cols.COUNTERPART_COLUMN:
                return reader.column_map[TransactionCSVColumns.COUNTERPART]
            elif column == self.cols.ACCOUNT_COLUMN:
                return reader.column_map[TransactionCSVColumns.ACCOUNT]
            elif column == self.cols.NOTE_COLUMN:
                return reader.column_map[TransactionCSVColumns.NOTE]
            else:
                raise NotImplementedError(f"DisplayRole for column {column} is not implemented."
                                          f"Accepted columns: {self.cols}")
        elif role == Qt.ItemDataRole.EditRole:
            if column == self.cols.NAME:
                return reader.name
            elif column == self.cols.DATE_COLUMN:
                return reader.column_map[TransactionCSVColumns.DATE]
            elif column == self.cols.AMOUNT_COLUMN:
                return reader.column_map[TransactionCSVColumns.AMOUNT]
            elif column == self.cols.COUNTERPART_COLUMN:
                return reader.column_map[TransactionCSVColumns.COUNTERPART]
            elif column == self.cols.ACCOUNT_COLUMN:
                return reader.column_map[TransactionCSVColumns.ACCOUNT]
            elif column == self.cols.NOTE_COLUMN:
                return reader.column_map[TransactionCSVColumns.NOTE]
            else:
                raise NotImplementedError(f"EditRole for column {column} is not implemented."
                                          f"Accepted columns: {self.cols}")
        return None

    def setData(
        self, index=QModelIndex(), value=None, role=Qt.ItemDataRole.EditRole
    ) -> bool:
        if not index.isValid():
            return False

        item: TransactionsCSVReader = self.get_item(index)
        column = index.column()

        if role == Qt.ItemDataRole.EditRole:
            if column == self.cols.NAME:
                item.name = value
                self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                return True
            elif column == self.cols.DATE_COLUMN:
                item.column_map[TransactionCSVColumns.DATE] = int(value)
                self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                return True
            elif column == self.cols.AMOUNT_COLUMN:
                item.column_map[TransactionCSVColumns.AMOUNT] = int(value)
                self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                return True
            elif column == self.cols.COUNTERPART_COLUMN:
                item.column_map[TransactionCSVColumns.COUNTERPART] = int(value)
                self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                return True
            elif column == self.cols.ACCOUNT_COLUMN:
                item.column_map[TransactionCSVColumns.ACCOUNT] = int(value)
                self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                return True
            elif column == self.cols.NOTE_COLUMN:
                item.column_map[TransactionCSVColumns.NOTE] = int(value)
                self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                return True
            else:
                NotImplementedError(f"EditRole for column {column} is not implemented."
                                    f"Accepted columns: {self.cols}")

        return False

    def headerData(self, section, orientation, /, role = ...):
        if orientation == Qt.Orientation.Vertical:
            return None
        if section < 0:
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            if section == self.cols.NAME:
                return "Name"
            elif section == self.cols.DATE_COLUMN:
                return "Date Column"
            elif section == self.cols.AMOUNT_COLUMN:
                return "Amount Column"
            elif section == self.cols.COUNTERPART_COLUMN:
                return "Counterpart Column"
            elif section == self.cols.ACCOUNT_COLUMN:
                return "Account Column"
            elif section == self.cols.NOTE_COLUMN:
                return "Note Column"
            else:
                raise NotImplementedError(f"DisplayRole for section {section} is not implemented."
                                          f"Accepted sections: {self.cols}")
        elif role == Qt.ItemDataRole.ToolTipRole:
            if section == self.cols.NAME:
                return "Specifies the name of your reader"
            elif section == self.cols.DATE_COLUMN:
                return ("Specifies in which column the reader finds information about the transaction date.\n"
                        "The column in the .csv file should be a valid date.\n"
                        "If left empty, this data will not be read from the .csv file.")
            elif section == self.cols.AMOUNT_COLUMN:
                return ("Specifies in which column the reader finds information about the transaction amount.\n"
                        "The column in the .csv file should be a valid amount.\n"
                        "If left empty, this data will not be read from the .csv file.")
            elif section == self.cols.COUNTERPART_COLUMN:
                return ("Specifies in which column the reader finds information about the transaction counterpart.\n"
                        "The column in the .csv file should be a valid IBAN.\n"
                        "If left empty, this data will not be read from the .csv file.")
            elif section == self.cols.ACCOUNT_COLUMN:
                return ("Specifies in which column the reader finds information about the transaction bank account.\n"
                        "The column in the .csv file should be a valid IBAN.\n"
                        "If left empty, this data will not be read from the .csv file.")
            elif section == self.cols.NOTE_COLUMN:
                return ("Specifies in which column the reader finds information about the transaction note.\n"
                        "If left empty, this data will not be read from the .csv file.")
            else:
                raise NotImplementedError(f"ToolTipRole for section {section} is not implemented."
                                          f"Accepted sections: {self.cols}")

        return None

    def flags(self, index, /):
        """
        Returns the item flags for the given index.
        Indicates that the item is selectable, editable, and enabled.
        """
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled
