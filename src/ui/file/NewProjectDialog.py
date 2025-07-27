from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.models.Projects import ProjectsModel
from src.paths import IconPaths


class NewProjectDialog(QDialog):

    def __init__(self, projects_model: ProjectsModel, parent: QWidget):
        super(NewProjectDialog, self).__init__(parent)
        self._projects_model = projects_model

        self.setWindowTitle("New Project")

        self._layout = QVBoxLayout(self)

        # Add input line
        choose_directory_widget = QWidget(self)
        choose_directory_layout = QHBoxLayout(choose_directory_widget)
        self._choose_directory_line_edit = QLineEdit(parent=choose_directory_widget)
        self._choose_directory_line_edit.setPlaceholderText("Choose directory")
        choose_directory_button = QPushButton(parent=choose_directory_widget)
        choose_directory_button.setIcon(QIcon(str(IconPaths.FOLDER)))
        choose_directory_button.clicked.connect(self._open_folder_dialog)

        choose_directory_layout.addWidget(QLabel("Project Directory"))
        choose_directory_layout.addWidget(self._choose_directory_line_edit)
        choose_directory_layout.addWidget(choose_directory_button)

        # Add button box
        self._button_box = QDialogButtonBox(Qt.Horizontal)
        self._button_box.accepted.connect(self._clicked_create_new_project)
        self._button_box.rejected.connect(self.reject)
        create_button = self._button_box.addButton(
            "Create", QDialogButtonBox.ButtonRole.AcceptRole
        )
        cancel_button = self._button_box.addButton(
            "Cancel", QDialogButtonBox.ButtonRole.RejectRole
        )

        # Add all to layout
        self._layout.addWidget(choose_directory_widget)
        self._layout.addStretch()
        self._layout.addWidget(self._button_box)

    def _clicked_create_new_project(self):
        project_dir = self._choose_directory_line_edit.text()
        self._projects_model.create_new_project(project_directory=project_dir)
        self.accept()

    def _open_folder_dialog(self):
        directory_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self._choose_directory_line_edit.setText(directory_path)
