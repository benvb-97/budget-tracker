from typing import Optional, TYPE_CHECKING, Any

from src.data.Currencies import Currencies
from src.data.TaggedItems import TaggedItemsType
from src.data.settings.AppSettings import AppSettings
from src.data.settings.GeneralSettings import GeneralSettingKeys
from src.models.TaggedItems import TaggedItemsOverviewTableModel
from src.utils.input_processing import convert_string_to_amount

if TYPE_CHECKING:
    from src.data.Projects import Project
    from src.models.Projects import ProjectsModel
from src.data.Transactions import Transactions, Transaction
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QDate
from enum import IntEnum
import datetime


class Columns(IntEnum):

    IDENTIFIER = 0
    DATE = 1
    AMOUNT = 2
    COUNTERPART = 3
    CATEGORY = 4
    ACCOUNT = 5
    NOTE = 6


class TransactionsOverviewTableModel(TaggedItemsOverviewTableModel):
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

    def _setup_connections(self):
        super()._setup_connections()

        # Pass categories model updates to relevant comboBox
        self._projects_model.transaction_categories_model.dataChanged.connect(
            lambda: self._update_comboBox_delegates(self.cols.CATEGORY)
        )
        # Pass bank accounts model updates to relevant comboBox
        self._projects_model.bank_accounts_model.dataChanged.connect(
            lambda: self._update_comboBox_delegates(self.cols.ACCOUNT)
        )
        # Pass counterparts model updates to relevant comboBox
        self._projects_model.counterparts_model.dataChanged.connect(
            lambda: self._update_comboBox_delegates(self.cols.COUNTERPART)
        )

    def _get_project_data(self, project: "Project") -> TaggedItemsType:
        return project.transactions

    def data(self, index=QModelIndex(), role=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None

        column = index.column()
        transaction = self.get_item(index)  # type: Transaction

        if role == Qt.ItemDataRole.DisplayRole:
            if column == self.cols.IDENTIFIER:
                return f"{transaction.identifier}"
            elif column == self.cols.DATE:
                qdate = QDate(transaction.date.year, transaction.date.month, transaction.date.day)
                return qdate

            elif column == self.cols.AMOUNT:
                return f"{transaction.amount}"
            elif column == self.cols.COUNTERPART:
                return f"{transaction.counterpart.name if transaction.counterpart is not None else ''}"
            elif column == self.cols.CATEGORY:
                return f"{transaction.category.name if transaction.category is not None else ''}"
            elif column == self.cols.ACCOUNT:
                return f"{transaction.account.name if transaction.account is not None else ''}"
            elif column == self.cols.NOTE:
                return transaction.note
            else:
                raise NotImplementedError(f"DisplayRole for column {column} is not implemented."
                                          f"Accepted columns: {self.cols}")

        elif role == Qt.ItemDataRole.EditRole:
            if column == self.cols.DATE:
                qdate = QDate(transaction.date.year, transaction.date.month, transaction.date.day)
                return qdate
            elif column == self.cols.AMOUNT:
                return f"{transaction.amount}"
            elif column == self.cols.COUNTERPART:
                return transaction.counterpart.identifier if transaction.counterpart is not None else None
            elif column == self.cols.CATEGORY:
                return transaction.category.identifier if transaction.category is not None else None
            elif column == self.cols.ACCOUNT:
                return transaction.account.identifier if transaction.account is not None else None

        elif role == self.comboBoxOptionsRole:
            if column == self.cols.ACCOUNT:
                accounts = self._projects_model.current_project.bank_accounts
                return {identifier: account.name for identifier, account in accounts.items()}
            elif column == self.cols.CATEGORY:
                categories = self._projects_model.current_project.transaction_categories
                return {identifier: category.name for identifier, category in categories.items()}
            elif column == self.cols.COUNTERPART:
                counterparts = self._projects_model.current_project.counterparts
                return {identifier: counterpart.name for identifier, counterpart in counterparts.items()}
            else:
                return {}
        return None

    def setData(
        self, index=QModelIndex(), value=None, role=Qt.ItemDataRole.EditRole
    ) -> bool:
        if not index.isValid():
            return False

        column = index.column()
        transaction = self.get_item(index)  # type: Transaction

        if role == Qt.ItemDataRole.EditRole:
            if column == self.cols.DATE:
                qdate: QDate = value
                new_date = datetime.date(qdate.year(), qdate.month(), qdate.day())
                transaction.date = new_date
                self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                return True

            elif column == self.cols.AMOUNT:
                amount = convert_string_to_amount(value)
                if amount is not None:
                    transaction.amount = amount
                    self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                    return True
                return False

            elif column == self.cols.COUNTERPART:
                identifier = value
                if identifier is None or type(identifier) is not int:  # No valid selection, set to None
                    transaction.counterpart = None
                    self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                    return True

                counterparts = self._projects_model.current_project.counterparts
                if identifier in counterparts:
                    transaction.counterpart = counterparts[identifier]
                    self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                    return True
                return False

            elif column == self.cols.CATEGORY:
                identifier = value
                if identifier is None or type(identifier) is not int:  # No valid selection, set to None
                    transaction.category = None
                    self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                    return True

                categories = self._projects_model.current_project.transaction_categories
                if identifier in categories:
                    transaction.category = categories[identifier]
                    self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                    return True
                return False

            elif column == self.cols.ACCOUNT:
                identifier = value
                if identifier is None or type(identifier) is not int:  # No valid selection, set to None
                    transaction.account = None
                    self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                    return True

                accounts = self._projects_model.current_project.bank_accounts
                if identifier in accounts:
                    transaction.account = accounts[identifier]
                    self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole)
                    return True
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

    def _update_comboBox_delegates(self, column: int) -> None:
        """
        Lets the UI know that it should update the contents and model of a specific comboBox delegate.
        -> useful when the model on which the comboBox contents rely, changes.
        """

        top_left = self.index(0, column)
        bottom_right = self.index(self.rowCount(), column)

        self.dataChanged.emit(top_left, bottom_right,
                              Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole | self.comboBoxOptionsRole,
                              )
