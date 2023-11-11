import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction
from registry.command_registry import CommandRegistry
from controllers.file_controller import FileController
from controllers.command_controller import CommandController
from views.track_selection_dialog import TrackSelectionDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)  # Use this layout for all widgets

        self.controller = FileController(self)
        self.command_controller = CommandController()
        self.setup_ui()
        self.setup_menu_bar()


    def setup_ui(self):
        self.setWindowTitle("MKV and Subtitle Tool")
        self.setGeometry(100, 100, 800, 600)

        # List widgets
        self.mkv_list = QListWidget()
        self.mkv_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.subtitle_list = QListWidget()
        self.subtitle_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.layout.addWidget(self.mkv_list)  # Add to the central layout
        self.layout.addWidget(self.subtitle_list)

        # Buttons
        open_file_button = QPushButton("Open Files")
        open_file_button.clicked.connect(lambda: self.controller.open_file_dialog(True))
        self.layout.addWidget(open_file_button)  # Add to the central layout

        open_folder_button = QPushButton("Open Folder")
        open_folder_button.clicked.connect(lambda: self.controller.open_file_dialog(False))
        self.layout.addWidget(open_folder_button)  # Add to the central layout

    def setup_menu_bar(self):
        self.menu_bar = self.menuBar()  # Create the menu bar
        self.commands_menu = self.menu_bar.addMenu("Commands")

        for name, command_class in CommandRegistry.get_commands().items():
            action = QAction(name, self)
            action.triggered.connect(lambda checked, c=command_class: self.on_command_triggered(c))
            self.commands_menu.addAction(action)
    

    def on_command_triggered(self, command_class):
        selected_files = self.get_selected_files()  # Implement this method
        self.command_controller.execute_command(command_class, selected_files)

    def add_to_list(self, list_widget, file_path):
        list_widget.addItem(file_path)

    def get_selected_files(self):
        selected_files = {
            'mkv': [],
            'subs': []
        }

        # Get selected MKV files
        for item in self.mkv_list.selectedItems():
            selected_files['mkv'].append(item.text())

        # Get selected subtitle files
        for item in self.subtitle_list.selectedItems():
            selected_files['subs'].append(item.text())

        return selected_files
    

    

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
