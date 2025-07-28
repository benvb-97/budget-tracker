from typing import Optional, TYPE_CHECKING, Any

from src.data.Currencies import Currencies
from src.data.TaggedItems import TaggedItemsType
from src.data.settings.AppSettings import AppSettings
from src.data.settings.GeneralSettings import GeneralSettingKeys
from src.models.TaggedItems import TaggedItemsOverviewTableModel

if TYPE_CHECKING:
    from src.data.Projects import Project
from src.data.Transactions import Transactions, Transaction
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from enum import IntEnum
from src.models.Projects import ProjectsModel


class Columns(IntEnum):

    IDENTIFIER = 0
    DATE = 1
    AMOUNT = 2
    COUNTERPART = 3
    CATEGORY = 4
    ACCOUNT = 5
    NOTE = 6


class IncomeTransactionsOverviewTableModel(TaggedItemsOverviewTableModel):
    cols = Columns
    comboBox_columns = (Columns.COUNTERPART,
                        Columns.CATEGORY,
                        Columns.ACCOUNT,)

    comboBoxOptionsRole = Qt.ItemDataRole.UserRole

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
        return project.income_transactions

    def data(self, index=QModelIndex(), role=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None

        column = index.column()
        transaction = self.get_item(index)  # type: Transaction

        if role == Qt.ItemDataRole.DisplayRole:
            if column == self.cols.IDENTIFIER:
                return f"{transaction.identifier}"
            elif column == self.cols.DATE:
                return f"{transaction.date}"
            elif column == self.cols.AMOUNT:
                return f"{transaction.amount}"
            elif column == self.cols.COUNTERPART:
                return f"{transaction.counterpart}"
            elif column == self.cols.CATEGORY:
                return f"{transaction.category}"
            elif column == self.cols.ACCOUNT:
                return f"{transaction.account}"
            elif column == self.cols.NOTE:
                return transaction.note
            else:
                raise NotImplementedError(f"DisplayRole for column {column} is not implemented."
                                          f"Accepted columns: {self.cols}")
        elif role == self.comboBoxOptionsRole:
                return {}

        return None

    def setData(
        self, index=QModelIndex(), value=None, role=Qt.ItemDataRole.EditRole
    ) -> bool:
        if not index.isValid():
            return False

        return False

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if orientation == Qt.Orientation.Vertical:
            return None
        if section < 0:
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            if section == self.cols.IDENTIFIER:
                return f"ID"
            elif section == self.cols.DATE:
                return "Date"
            elif section == self.cols.AMOUNT:
                currency_symbol = Currencies[self._settings.general[GeneralSettingKeys.CURRENCY].value].symbol
                return f"Amount [{currency_symbol}]"
            elif section == self.cols.COUNTERPART:
                return f"Counterpart"
            elif section == self.cols.CATEGORY:
                return f"Category"
            elif section == self.cols.ACCOUNT:
                return f"Account"
            elif section == self.cols.NOTE:
                return "Note"
            else:
                raise NotImplementedError(f"DisplayRole for section {section} is not implemented."
                                          f"Accepted sections: {self.cols}")
        else:
            return None

    def flags(self, index=QModelIndex()):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        column = index.column()
        if column in [self.cols.IDENTIFIER]:  # Name, Note
            return (
                Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsSelectable
            )
        else:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable