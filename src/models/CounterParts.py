import logging
from typing import Optional, TYPE_CHECKING, Any

from src.data.Currencies import Currencies
from src.data.TaggedItems import TaggedItemsType
from src.data.TransactionCategories import TransactionCategory
from src.data.settings.AppSettings import AppSettings
from src.data.settings.GeneralSettings import GeneralSettingKeys
from src.models.TaggedItems import TaggedItemsOverviewTableModel, TaggedItemsListModel

if TYPE_CHECKING:
    from src.data.Projects import Project
    from src.models.Projects import ProjectsModel
from src.data.Transactions import Transactions, IncomeTransaction
from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, QAbstractTableModel
from enum import IntEnum
from src.data.CounterParts import CounterPart
from schwifty.iban import IBAN


class CounterPartsOverviewListModel(TaggedItemsListModel):

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
        return project.counterparts

    def data(self, index=QModelIndex(), role=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None

        counterpart = self.get_item(index)  # type: CounterPart

        if role == Qt.ItemDataRole.DisplayRole:
            return counterpart.name
        elif role == Qt.ItemDataRole.EditRole:
            return counterpart.name
        return None

    def setData(
        self, index=QModelIndex(), value=None, role=Qt.ItemDataRole.EditRole
    ) -> bool:
        if not index.isValid():
            return False

        item: CounterPart = self.get_item(index)

        if role == Qt.ItemDataRole.EditRole:
            item.name = value
            self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole)
            return True

        return False

    def flags(self, index, /):
        """
        Returns the item flags for the given index.
        Indicates that the item is selectable, editable, and enabled.
        """
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled


class CounterPartDataRows(IntEnum):
    IBAN = 0
    NOTE = 1


class CounterPartDataModel(QAbstractTableModel):

    rows = CounterPartDataRows

    def __init__(self,
                 counterparts_model: "CounterPartsOverviewListModel",
                 settings: AppSettings,
                 parent,
                 ) -> None:
        super().__init__(parent)

        self._counterparts_model = counterparts_model
        self._current_counterpart = None  # type: Optional[CounterPart]  # Placeholder, to be initialized later during init
        self._settings = settings

        self._setup_connections()
        self._set_current_counterpart()  # Initializes current counterpart

    def _setup_connections(self) -> None:
        self._counterparts_model.current_item_changed.connect(self._set_current_counterpart)

    def _set_current_counterpart(self):
        self.beginResetModel()
        new_counterpart: Optional[CounterPart] = self._counterparts_model.current_item
        self._current_counterpart = new_counterpart
        self.endResetModel()

    def rowCount(self, /, parent = ...):
        return len(self.rows) if self._current_counterpart is not None else 0

    def columnCount(self, /, parent = ...):
        return 1

    def data(self, index=QModelIndex(), role=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or self._current_counterpart is None:
            return None

        row = index.row()

        if role == Qt.ItemDataRole.DisplayRole:
            if row == self.rows.IBAN:
                return str(self._current_counterpart.iban) if self._current_counterpart.iban is not None else "Enter a valid IBAN here..."
            elif row == self.rows.NOTE:
                return self._current_counterpart.note
            else:
                raise NotImplementedError(f"DisplayRole for row {row} is not implemented."
                                          f"Accepted row: {self.rows}")
        elif role == Qt.ItemDataRole.EditRole:
            if row == self.rows.IBAN:
                return str(self._current_counterpart.iban) if self._current_counterpart.iban is not None else ""
            elif row == self.rows.NOTE:
                return self._current_counterpart.note
            else:
                raise NotImplementedError(f"EditRole for row {row} is not implemented."
                                          f"Accepted row: {self.rows}")

        return None

    def setData(
        self, index=QModelIndex(), value=None, role=Qt.ItemDataRole.EditRole
    ) -> bool:
        if not index.isValid() or self._current_counterpart is None:
            return False

        row = index.row()

        if role == Qt.ItemDataRole.EditRole:
            if row == self.rows.IBAN:

                new_iban = IBAN(value, allow_invalid=True)
                if not new_iban.is_valid:
                    logging.getLogger(__name__).warning(f"Passed an invalid IBAN: {value}")
                    return False

                self._current_counterpart.iban = new_iban
                self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole)
                return True
            elif row == self.rows.NOTE:
                self._current_counterpart.note = value
                self.dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole)
                return True

        return False

    def headerData(self, section, orientation, /, role = ...):
        if self._current_counterpart is None or section < 0 or orientation == Qt.Orientation.Horizontal:
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            if section == self.rows.IBAN:
                return "IBAN"
            elif section == self.rows.NOTE:
                return "Note"
        elif role == Qt.ItemDataRole.ToolTipRole:
            if section == self.rows.IBAN:
                return "Enter a valid IBAN number here for your counter part"
            elif section == self.rows.NOTE:
                return "Optional, add a note to your counter part"
        return None

    def flags(self, index, /):
        """
        Returns the item flags for the given index.
        Indicates that the item is selectable, editable, and enabled.
        """
        if not index.isValid() or self._current_counterpart is None:
            return Qt.ItemFlag.NoItemFlags

        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled
