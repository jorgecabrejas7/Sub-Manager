from pathlib import Path
from PyQt6.QtWidgets import QFileDialog
from models.file_model import MKVFile, SubtitleFile

class FileController:
    def __init__(self, view):
        self.view = view
        self.loaded_mkv_files = set()
        self.loaded_subtitle_files = set()

    def open_file_dialog(self, multiple_files=True):
        if multiple_files:
            files, _ = QFileDialog.getOpenFileNames(self.view, "Select Files", "", 
                                                   "All Files (*);;MKV Files (*.mkv);;Subtitle Files (*.srt *.ass)")
            files = [Path(file) for file in files]  # Convert to Path objects
        else:
            dir = QFileDialog.getExistingDirectory(self.view, "Select Folder", "")
            if dir:
                directory = Path(dir)
                files = [file for file in directory.iterdir() if file.is_file()]
            else:
                files = []

        self.process_selected_files(files)

    def process_selected_files(self, files):
        for file_path in files:
            path = Path(file_path)  # Using pathlib for path manipulation

            if path.suffix.lower() in ['.mkv']:
                if path not in self.loaded_mkv_files:
                    self.loaded_mkv_files.add(path)
                    mkv_file = MKVFile(path)
                    self.view.add_to_list(self.view.mkv_list, str(mkv_file.file_path))
            elif path.suffix.lower() in ['.srt', '.ass']:
                if path not in self.loaded_subtitle_files:
                    self.loaded_subtitle_files.add(path)
                    subtitle_file = SubtitleFile(path)
                    self.view.add_to_list(self.view.subtitle_list, str(subtitle_file.file_path))

        print("Loaded MKV Files:", self.loaded_mkv_files)
        print("Loaded Subtitle Files:", self.loaded_subtitle_files)