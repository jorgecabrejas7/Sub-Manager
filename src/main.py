import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
import pkgutil
import importlib
import os


def load_all_commands(directory):
    for (_, module_name, _) in pkgutil.iter_modules([directory]):
        # Import the module
        importlib.import_module('.' + module_name, package='commands')

def main():
    commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
    load_all_commands(commands_dir)
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()