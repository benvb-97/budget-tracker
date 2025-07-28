from typing import Optional, TYPE_CHECKING, Any

from src.data.Currencies import Currencies
from src.data.TaggedItems import TaggedItemsType
from src.data.TransactionCategories import TransactionCategory
from src.data.settings.AppSettings import AppSettings
from src.data.settings.GeneralSettings import GeneralSettingKeys
from src.models.TaggedItems import TaggedItemsOverviewTableModel, TaggedItemsListModel

if TYPE_CHECKING:
    from src.data.Projects import Project
from src.data.Transactions import Transactions, Transaction
from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
from enum import IntEnum
from src.models.Projects import ProjectsModel

class Columns(IntEnum):
    NAME = 0
    NOTE = 1


class IncomeCategoriesOverviewModel(TaggedItemsOverviewTableModel):
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
        return project.income_categories

    def data(self, index=QModelIndex(), role=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None

        category = self.get_item(index)  # type: TransactionCategory
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if column == self.cols.NAME:
                return category.name
            elif column == self.cols.NOTE:
                return category.note
            else:
                raise NotImplementedError(f"DisplayRole for column {column} is not implemented."
                                          f"Accepted columns: {self.cols}")
        elif role == Qt.ItemDataRole.EditRole:
            if column == self.cols.NAME:
                return category.name
            elif column == self.cols.NOTE:
                return category.note
            else:
                raise NotImplementedError(f"EditRole for column {column} is not implemented."
                                          f"Accepted columns: {self.cols}")
        return None

    def setData(
        self, index=QModelIndex(), value=None, role=Qt.ItemDataRole.EditRole
    ) -> bool:
        if not index.isValid():
            return False

        item: TransactionCategory = self.get_item(index)
        column = index.column()

        if role == Qt.ItemDataRole.EditRole:
            if column == self.cols.NAME:
                item.name = value
                self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole)
                return True
            elif column == self.cols.NOTE:
                item.note = value
                self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole)
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
            elif section == self.cols.NOTE:
                return "Note"
            else:
                raise NotImplementedError(f"DisplayRole for section {section} is not implemented."
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
