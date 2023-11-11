from PyQt6.QtWidgets import QMessageBox
import traceback

class CommandController:
    def __init__(self):
        pass  # Add any initialization logic if needed

    def execute_command(self, command_class, selected_files):
        try:
            command = command_class(selected_files)
            command.execute()
        except Exception as e:
            traceback.print_exc()
            self.show_error_dialog(str(e))

    def show_error_dialog(self, error_message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("An error occurred")
        msg.setInformativeText(error_message)
        msg.setWindowTitle("Error")
        msg.exec()