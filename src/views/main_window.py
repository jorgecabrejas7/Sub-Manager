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

        # Create a grid layout for the buttons
        button_layout = QGridLayout()

        # Create the buttons
        open_file_button = QPushButton("Open Files")
        open_file_button.clicked.connect(lambda: self.controller.open_file_dialog(True))

        open_folder_button = QPushButton("Open Folder")
        open_folder_button.clicked.connect(lambda: self.controller.open_file_dialog(False))

        self.clear_mkv_button = QPushButton("Clear MKV Files")
        self.clear_mkv_button.clicked.connect(self.clear_mkv_files)

        self.clear_sub_button = QPushButton("Clear Subtitle Files")
        self.clear_sub_button.clicked.connect(self.clear_sub_files)

        select_all_button = QPushButton("Select All Files")
        select_all_button.clicked.connect(self.select_all_files)

        deselect_all_button = QPushButton("Deselect All Files")
        deselect_all_button.clicked.connect(self.deselect_all_files)

        # Add the buttons to the grid layout
        button_layout.addWidget(open_file_button, 0, 0)
        button_layout.addWidget(open_folder_button, 0, 1)
        button_layout.addWidget(self.clear_mkv_button, 1, 0)
        button_layout.addWidget(self.clear_sub_button, 1, 1)
        button_layout.addWidget(select_all_button, 2, 0)
        button_layout.addWidget(deselect_all_button, 2, 1)

        # Add the grid layout to the central layout
        self.layout.addLayout(button_layout)

    def deselect_all_files(self):
        self.mkv_list.clearSelection()
        self.subtitle_list.clearSelection()

    def select_all_files(self):
        self.mkv_list.selectAll()
        self.subtitle_list.selectAll()

    def clear_mkv_files(self):
        # Clear the MKV file list
        self.mkv_list.clear()

    def clear_sub_files(self):
        # Clear the subtitle file list
        self.subtitle_list.clear()

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
