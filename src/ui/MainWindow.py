from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()

        self.showMaximized()