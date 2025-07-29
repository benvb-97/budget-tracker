from typing import TYPE_CHECKING

from PySide6.QtCore import QItemSelectionModel, QModelIndex, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHeaderView,
    QListView,
    QMenu,
    QPushButton,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.data.settings.AppSettings import AppSettings
from src.models.CounterParts import CounterPartsOverviewListModel, CounterPartDataModel
from src.models.Projects import ProjectsModel


class CounterPartsListView(QListView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)

    def open_context_menu(self, position):
        """
        Opens at right-click
        """
        index = self.indexAt(position)  # type: QModelIndex

        if index.isValid():
            model: CounterPartsOverviewListModel = index.model()

            menu = QMenu(self)

            # Add actions to the context menu
            delete_action = QAction("Delete counter part", self)
            delete_action.triggered.connect(lambda: model.delete_item(index))
            menu.addAction(delete_action)

            # Show the menu at the cursor position
            menu.exec(self.viewport().mapToGlobal(position))


class ManageCounterPartsDialog(QDialog):
    def __init__(self,
                 projects_model: "ProjectsModel",
                 settings: AppSettings,
                 parent):
        super().__init__(parent)

        self._projects_model = projects_model
        self._settings = settings

        self._setup_ui()
        self._set_models()
        self._setup_connections()

    def _setup_ui(self) -> None:
        self.setWindowTitle("Manage Counter Parts")

        self._layout = QVBoxLayout(self)
        self._splitter = QSplitter(self)
        self._layout.addWidget(self._splitter)

        # 1. Left part of splitter: list of bank counterparts and button to create more
        self._counterparts_view = CounterPartsListView(self)
        self._counterparts_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems
        )
        self._counterparts_view.setHorizontalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )

        self._new_counterpart_button = QPushButton("New Counterpart", self)

        counterparts_widget = QWidget(self)
        counterparts_layout = QVBoxLayout(counterparts_widget)
        counterparts_layout.addWidget(self._counterparts_view)
        counterparts_layout.addStretch()
        counterparts_layout.addWidget(self._new_counterpart_button)
        self._splitter.addWidget(counterparts_widget)

        # Right part of splitter: list of values within set and button to create more
        self._counterpart_view = QTableView(self)

        self._counterpart_header_view = QHeaderView(
            Qt.Orientation.Vertical, self._counterpart_view
        )
        self._counterpart_header_view.setDefaultAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Align header text center
        self._counterpart_view.setVerticalHeader(self._counterpart_header_view)
        self._counterpart_view.horizontalHeader().setStretchLastSection(True)
        self._counterpart_view.horizontalHeader().hide()

        counterpart_widget = QWidget(self)
        counterpart_layout = QVBoxLayout(counterpart_widget)
        counterpart_layout.addWidget(self._counterpart_view)
        counterpart_layout.addStretch()
        self._splitter.addWidget(counterpart_widget)

    def _set_models(self) -> None:
        self._counterparts_model = self._projects_model.counterparts_model
        self._counterpart_model = CounterPartDataModel(counterparts_model=self._counterparts_model, settings=self._settings, parent=self)

        self._counterpart_selection_model = QItemSelectionModel(self._counterparts_model)

        self._counterparts_view.setModel(self._counterparts_model)
        self._counterparts_view.setSelectionModel(self._counterpart_selection_model)

        self._counterpart_view.setModel(self._counterpart_model)
        self._counterpart_header_view.setModel(self._counterpart_model)

    def _setup_connections(self) -> None:
        self._counterpart_selection_model.selectionChanged.connect(
            self._counterparts_model.change_selection
        )
        self._new_counterpart_button.clicked.connect(self._counterparts_model.create_new_item)
