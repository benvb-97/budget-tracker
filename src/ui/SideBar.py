from PySide6.QtCore import QItemSelectionModel, QModelIndex, QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QAbstractItemView,
    QLabel,
    QListView,
    QMenu,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from src.models.Projects import ProjectsModel


class ProjectsListView(QListView):

    def mousePressEvent(self, event):
        # Get the index at the click position
        index = self.indexAt(event.pos())
        # Check if the index is valid (meaning the click is on an actual item)
        if index.isValid():
            # If it's a valid item, pass the event to the base class for normal selection behavior
            super().mousePressEvent(event)
        else:
            # Ignore the click outside any item to prevent deselection
            event.ignore()


class SideBar(QWidget):
    def __init__(
        self,
        parent,
        projects_model: ProjectsModel,
    ):
        super(SideBar, self).__init__(parent=parent)
        self._projects_model = projects_model

        self._setup_ui()
        self._set_models()
        self._setup_connections()

    def _setup_ui(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        self._layout = QVBoxLayout(self)

        # Projects label
        projects_header = QLabel("Project Explorer")
        projects_header.setMinimumSize(1, 1)
        self._layout.addWidget(projects_header, alignment=Qt.AlignmentFlag.AlignCenter)

        # Projects view
        self._projects_view = ProjectsListView()
        self._projects_view.setAlternatingRowColors(True)
        self._projects_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems
        )
        self._projects_view.setHorizontalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self._layout.addWidget(self._projects_view)

    def _set_models(self) -> None:
        self._project_selection_model = QItemSelectionModel(self._projects_model)
        self._projects_view.setModel(self._projects_model)
        self._projects_view.setSelectionModel(self._project_selection_model)

    def _setup_connections(self) -> None:
        self._project_selection_model.selectionChanged.connect(
            self._projects_model.change_selection
        )

    def sizeHint(
        self,
    ) -> (
        QSize
    ):  # Provide reasonable initial width for side bar (50), height doesn't matter
        return QSize(100, 1)