"""
Sets are lists of integers or floats that can be assigned to a parametric variable to define the values that the
parametric variable can assume
"""

from enum import IntEnum
from typing import Any, Optional, TYPE_CHECKING

from src.data.settings.AppSettings import AppSettings

if TYPE_CHECKING:
    from src.data.Projects import Project
    from src.models.Projects import ProjectsModel

from PySide6.QtCore import (
    QAbstractListModel,
    QAbstractTableModel,
    QItemSelection,
    QModelIndex,
    Qt,
    Signal,
)
from PySide6.QtGui import QFont

from src.data.TaggedItems import TaggedItemType, TaggedItemsType, TaggedItems


class TaggedItemsListModel(QAbstractListModel):
    current_item_changed = Signal(object)

    def __init__(self, projects_model: "ProjectsModel", settings: AppSettings, parent):
        super().__init__(parent)

        self._projects_model = projects_model
        self._settings = settings

        self._data: Optional[TaggedItems] = None

        self._setup_connections()

        # Initialize data
        self._current_row = -1
        self._set_current_project_data(project=self._projects_model.current_project)

    def _setup_connections(self):
        """Sets up the signal-slot connections."""
        self._projects_model.current_project_changed.connect(self._set_current_project_data)

    def _set_current_project_data(self, project: Optional["Project"]):
        """Set new data based on current project"""
        self.beginResetModel()
        if project:
            self._data = self._get_project_data(project)
            self._row_to_id_map = {}  # type: dict[int, int]
            row = 0
            for item in self._data.values():
                self._row_to_id_map[row] = item.identifier
                row += 1
        else:
            self._data = None  # Use None to reset the view
            self._row_to_id_map = {}  # type: dict[int, int]
        self.endResetModel()

    def _get_project_data(self, project: "Project") -> TaggedItemsType:
        raise NotImplementedError

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._data) if self._data is not None else 0

    def data(self, index, role=...) -> Any:
        raise NotImplementedError

    def setData(self, index, value, role=...) -> bool:
        raise NotImplementedError

    def change_selection(self, selected: QItemSelection, deselected: QItemSelection):
        if deselected.empty():
            old_index = QModelIndex()
        else:
            old_index = deselected.indexes()[0]
        if selected.empty():
            new_index = QModelIndex()
        else:
            new_index = selected.indexes()[0]

        self._current_row = new_index.row()

        self.dataChanged.emit(new_index, new_index, [Qt.ItemDataRole.FontRole])
        self.dataChanged.emit(old_index, old_index, [Qt.ItemDataRole.FontRole])

        self.current_item_changed.emit(self.current_item)

    def create_new_item(
        self, identifier: int = None, json_dict: dict[str, Any] = None
    ) -> TaggedItemType:

        # Add to data
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        row = self.rowCount()
        new_item = self._data.create_new_item(
            identifier=identifier, json_dict=json_dict
        )
        self._row_to_id_map[row] = new_item.identifier
        self.endInsertRows()

        # set selection to new item
        if self._current_row:
            deselected_index = self.createIndex(self._current_row, 0)
            deselected = QItemSelection(deselected_index, deselected_index)
        else:
            deselected = QItemSelection(QModelIndex(), QModelIndex())

        selected_index = self.createIndex(row, 0)
        selected = QItemSelection(selected_index, selected_index)
        self.change_selection(selected=selected, deselected=deselected)

        return new_item

    def delete_item(self, delete_index: QModelIndex) -> None:
        assert delete_index.isValid(), f"{delete_index}"
        delete_row = delete_index.row()
        delete_item = self.get_item(delete_index)

        self.beginRemoveRows(QModelIndex(), delete_row, delete_row)
        self._data.delete_item(delete_item)
        _ = self._row_to_id_map.pop(delete_row)
        self.endRemoveRows()

        new_row_to_id_mapper = {}  # type: dict[int, int]
        row = 0
        for item in self._data.values():
            new_row_to_id_mapper[row] = item.identifier
            row += 1
        self._row_to_id_map = new_row_to_id_mapper

        # set selection to new project
        deselected = QItemSelection(QModelIndex(), QModelIndex())

        if len(self._data) > 0:
            selected_index = self.createIndex(0, 0)
            selected = QItemSelection(selected_index, selected_index)
        else:
            selected = QItemSelection(QModelIndex(), QModelIndex())

        self.change_selection(selected=selected, deselected=deselected)

    def copy_item(self, copy_index: QModelIndex) -> None:
        assert copy_index.isValid(), copy_index
        copy_row = copy_index.row()

        assert 0 <= copy_row < self.rowCount(), f"{copy_row}"

        old_item = self.get_item(copy_index)

        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        row = self.rowCount()
        new_item = self._data.copy_item(old_item)
        self._row_to_id_map[row] = new_item.identifier
        self.endInsertRows()

        # Set selection to copied item
        top_left = self.index(row, 0)
        bottom_right = self.index(row, 0)
        self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.DisplayRole])

        deselected_index = self.createIndex(copy_row, 0)
        deselected = QItemSelection(deselected_index, deselected_index)
        selected_index = self.createIndex(row, 0)
        selected = QItemSelection(selected_index, selected_index)
        self.change_selection(selected=selected, deselected=deselected)

    @property
    def current_item(self) -> Optional[Any]:
        return self.get_item(self.index(self._current_row, 0))

    def get_item(self, index: QModelIndex) -> Optional[Any]:
        if not index.isValid():
            return None

        return self._data[self._row_to_id_map[index.row()]]


class TaggedItemsOverviewTableModel(QAbstractTableModel):
    cols = None  # type: type[IntEnum]
    current_item_changed = Signal(object)

    def __init__(self, projects_model: "ProjectsModel", settings: AppSettings, parent):
        super().__init__(parent)

        self._projects_model = projects_model
        self._settings = settings

        self._data: Optional[TaggedItems] = None

        self._setup_connections()

        # Initialize data
        self._current_row = -1
        self._set_current_project_data(project=self._projects_model.current_project)

    def _setup_connections(self):
        """Sets up the signal-slot connections."""
        self._projects_model.current_project_changed.connect(self._set_current_project_data)

    def _set_current_project_data(self, project: Optional["Project"]):
        """Set new data based on current project"""
        self.beginResetModel()
        if project:
            self._data = self._get_project_data(project)
            self._row_to_id_map = {}  # type: dict[int, int]
            row = 0
            for item in self._data.values():
                self._row_to_id_map[row] = item.identifier
                row += 1
        else:
            self._data = None  # Use None to reset the view
            self._row_to_id_map = {}  # type: dict[int, int]
        self.endResetModel()

    def _get_project_data(self, project: "Project") -> TaggedItemsType:
        raise NotImplementedError

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._data) if self._data is not None else 0

    def columnCount(self, parent=...) -> int:
        return len(self.cols)

    def data(self, index, role=...) -> Any:
        raise NotImplementedError

    def setData(self, index, value, role=...) -> bool:
        raise NotImplementedError

    def change_selection(self, selected: QItemSelection, deselected: QItemSelection):
        if deselected.empty():
            old_index = QModelIndex()
        else:
            old_index = deselected.indexes()[0]
        if selected.empty():
            new_index = QModelIndex()
        else:
            new_index = selected.indexes()[0]

        self._current_row = new_index.row()

        self.dataChanged.emit(new_index, new_index, [Qt.ItemDataRole.FontRole])
        self.dataChanged.emit(old_index, old_index, [Qt.ItemDataRole.FontRole])

        self.current_item_changed.emit(self.current_item)

    def create_new_item(
        self, identifier: int = None, json_dict: dict[str, Any] = None
    ) -> TaggedItemType:

        # Add to data
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        row = self.rowCount()
        new_item = self._data.create_new_item(
            identifier=identifier, json_dict=json_dict
        )
        self._row_to_id_map[row] = new_item.identifier
        self.endInsertRows()

        # set selection to new item
        if self._current_row:
            deselected_index = self.createIndex(self._current_row, 0)
            deselected = QItemSelection(deselected_index, deselected_index)
        else:
            deselected = QItemSelection(QModelIndex(), QModelIndex())

        selected_index = self.createIndex(row, 0)
        selected = QItemSelection(selected_index, selected_index)
        self.change_selection(selected=selected, deselected=deselected)

        return new_item

    def delete_item(self, delete_index: QModelIndex) -> None:
        assert delete_index.isValid(), f"{delete_index}"
        delete_row = delete_index.row()
        delete_item = self.get_item(delete_index)

        self.beginRemoveRows(QModelIndex(), delete_row, delete_row)
        self._data.delete_item(delete_item)
        _ = self._row_to_id_map.pop(delete_row)
        self.endRemoveRows()

        new_row_to_id_mapper = {}  # type: dict[int, int]
        row = 0
        for item in self._data.values():
            new_row_to_id_mapper[row] = item.identifier
            row += 1
        self._row_to_id_map = new_row_to_id_mapper

        # set selection to new project
        deselected = QItemSelection(QModelIndex(), QModelIndex())

        if len(self._data) > 0:
            selected_index = self.createIndex(0, 0)
            selected = QItemSelection(selected_index, selected_index)
        else:
            selected = QItemSelection(QModelIndex(), QModelIndex())

        self.change_selection(selected=selected, deselected=deselected)

    def copy_item(self, copy_index: QModelIndex) -> None:
        assert copy_index.isValid(), copy_index
        copy_row = copy_index.row()

        assert 0 <= copy_row < self.rowCount(), f"{copy_row}"

        old_item = self.get_item(copy_index)

        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        row = self.rowCount()
        new_item = self._data.copy_item(old_item)
        self._row_to_id_map[row] = new_item.identifier
        self.endInsertRows()

        # Set selection to copied item
        top_left = self.index(row, 0)
        bottom_right = self.index(row, 0)
        self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.DisplayRole])

        deselected_index = self.createIndex(copy_row, 0)
        deselected = QItemSelection(deselected_index, deselected_index)
        selected_index = self.createIndex(row, 0)
        selected = QItemSelection(selected_index, selected_index)
        self.change_selection(selected=selected, deselected=deselected)

    @property
    def current_item(self) -> Optional[Any]:
        return self.get_item(self.index(self._current_row, 0))

    def get_item(self, index: QModelIndex) -> Optional[Any]:
        if not index.isValid():
            return None

        return self._data[self._row_to_id_map[index.row()]]
