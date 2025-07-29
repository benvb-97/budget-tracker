from typing import TYPE_CHECKING, Any, Optional

from PySide6.QtCore import QAbstractListModel, QItemSelection, QModelIndex, Qt, Signal
from PySide6.QtGui import QFont
import os

from src.data.settings.AppSettings import AppSettings
from src.models.BankAccounts import BankAccountsOverviewListModel
from src.models.CounterParts import CounterPartsOverviewListModel
from src.models.TransactionCategories import TransactionCategoriesOverviewModel
from src.models.Transactions import TransactionsOverviewTableModel

if TYPE_CHECKING:
    from src.data.Projects import Project, Projects


class ProjectsModel(QAbstractListModel):
    """Handles navigation between opened projects"""

    current_project_changed = Signal(object)

    def __init__(self, projects: "Projects", settings: AppSettings, parent):
        super().__init__(parent)

        self._settings = settings

        # Data
        self._projects = projects
        self._row_to_id_mapper = {}  # type: dict[int, int]
        row = 0
        for project in self._projects.values():
            self._row_to_id_mapper[row] = project.identifier

        self._current_row = 0 if self._projects else -1  # type: int

        self._create_models()

    def _create_models(self):
        self.bank_accounts_model = BankAccountsOverviewListModel(projects_model=self,
                                                                 settings=self._settings,
                                                                 parent=self)
        self.counterparts_model = CounterPartsOverviewListModel(projects_model=self,
                                                                settings=self._settings,
                                                                parent=self,
                                                                )

        self.transaction_categories_model = TransactionCategoriesOverviewModel(projects_model=self,
                                                                               settings=self._settings,
                                                                               parent=self,
                                                                               )
        self.transactions_model = TransactionsOverviewTableModel(projects_model=self,
                                                                 settings=self._settings,
                                                                 parent=self,
                                                                 )

    def rowCount(self, parent=QModelIndex()) -> int:
        return self._projects.n_projects

    def data(self, index=QModelIndex(), role=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or not self._projects:
            return None

        project: Project = self._get_project(index)

        if role == Qt.ItemDataRole.DisplayRole:
            return project.folder_name
        elif role == Qt.ItemDataRole.FontRole:
            font = QFont()
            if index.row() == self._current_row:
                font.setBold(True)
            return font
        else:
            return None

    def setData(
        self, index=QModelIndex(), value=None, role=Qt.ItemDataRole.EditRole
    ) -> bool:
        if not index.isValid():
            return False

        project = self._get_project(index)

        if role == Qt.ItemDataRole.EditRole:
            project.project_directory = value
            self.dataChanged.emit(
                index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]
            )
            return True
        else:
            return False

    def flags(self, index=QModelIndex()):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

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

        self.current_project_changed.emit(self.current_project)

    def create_new_project(self, project_directory: str) -> None:
        # add project to list
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        row = self.rowCount()
        project = self._projects.create_new_project(project_directory=project_directory)
        self._row_to_id_mapper[row] = project.identifier
        self.endInsertRows()

        # set selection to new project
        deselected_index = self.createIndex(self._current_row, 0)
        deselected = QItemSelection(deselected_index, deselected_index)

        selected_index = self.createIndex(row, 0)
        selected = QItemSelection(selected_index, selected_index)

        self.change_selection(selected=selected, deselected=deselected)

    def open_project(self, project_directory: str) -> None:
        # add project to list
        self.beginInsertRows(
            QModelIndex(), self.rowCount(QModelIndex()), self.rowCount(QModelIndex())
        )
        row = self.rowCount()
        project = self._projects.create_new_project(
            project_directory=project_directory, load_from_dir=True
        )
        self._row_to_id_mapper[row] = project.identifier
        self.endInsertRows()

        # set selection to new project
        deselected_index = self.createIndex(self._current_row, 0)
        deselected = QItemSelection(deselected_index, deselected_index)

        selected_index = self.createIndex(row, 0)
        selected = QItemSelection(selected_index, selected_index)

        self.change_selection(selected=selected, deselected=deselected)

    def save_current_project(self) -> None:
        current_project = self.current_project
        if current_project:
            current_project.save_project()

    def save_current_project_as(self, new_project_dir: str) -> None:
            current_project = self.current_project

            if os.path.isdir(new_project_dir):
                self._change_project_directory(project=current_project, new_project_directory=new_project_dir)
                current_project.save_project()

    def _change_project_directory(
        self, project: "Project", new_project_directory: str
    ) -> None:
        project_row = self._get_row(project)

        self.setData(
            self.createIndex(project_row, 0),
            new_project_directory,
            Qt.ItemDataRole.EditRole,
        )

    def save_all_projects(self) -> None:
        for project in self._projects.values():
            project.save_project()

    def close_current_project(self) -> None:
        if not self.has_project_opened:
            return

        self.beginRemoveRows(QModelIndex(), self.rowCount(), self.rowCount())
        _ = self._projects.pop(self.current_project.identifier)
        _ = self._row_to_id_mapper.pop(self._current_row)
        self.endRemoveRows()

        # update row mapper
        new_row_to_id_mapper = {}  # type: dict[int, int]
        row = 0
        for item in self._projects.values():
            new_row_to_id_mapper[row] = item.identifier
            row += 1
        self._row_to_id_mapper = new_row_to_id_mapper

        # set selection to new project
        deselected = QItemSelection(QModelIndex(), QModelIndex())

        if self._projects.n_projects > 0:
            selected_index = self.createIndex(0, 0)
            selected = QItemSelection(selected_index, selected_index)
        else:
            selected = QItemSelection(QModelIndex(), QModelIndex())

        self.change_selection(selected=selected, deselected=deselected)

    def close_all_projects(self) -> None:
        while self.has_project_opened is True:
            self.close_current_project()

    @property
    def has_project_opened(self) -> bool:
        return self._current_row != -1

    @property
    def current_project(self) -> Optional["Project"]:
        return self._get_project(self.index(self._current_row, 0))

    def _get_project(self, index: QModelIndex) -> Optional["Project"]:
        if not index.isValid():
            return None

        return self._projects[self._row_to_id_mapper[index.row()]]

    def _get_row(self, project: "Project") -> int:
        for row, identifier in self._row_to_id_mapper.items():
            if identifier == project.identifier:
                return row

        raise ValueError(f"{project.identifier}, {self._row_to_id_mapper.items()}")
