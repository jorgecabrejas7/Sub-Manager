from commands.command import Command
from PyQt6.QtWidgets import *
from PyQt6.QtCore import * 
from registry.register_command import register_command
import subprocess
from utils.mkv_utils import get_subtitle_tracks_ffmpeg
from views.track_selection_dialog import MainTrackSelectionDialog
import os
from concurrent.futures import ThreadPoolExecutor
import shutil
import tempfile

@register_command("Remove Subtitles")
class RemoveSubtitlesCommand(Command):
    def __init__(self, selected_files):
        self.selected_files = selected_files["mkv"]
        self.file_tracks = {}  # Dictionary to store the selected tracks for each file

    def execute(self):
        if not self.selected_files:  # Check if the list is empty
            QMessageBox.information(None, "No Files Selected", "No video files have been selected.")
            return

        # Prompt the user whether to keep the filenames the same and overwrite files
        overwrite = QMessageBox.question(None, "Overwrite Files", "Do you want to keep the filenames the same and overwrite files?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if overwrite == QMessageBox.StandardButton.Yes:
            self.overwrite = True
        else:
            self.overwrite = False

        # Ask the user for a folder
        self.output_folder = QFileDialog.getExistingDirectory(None, "Select Output Folder")

        use_same_tracks = False
        
        for file in self.selected_files:
            if not use_same_tracks:
                tracks = self.get_track_info(file)
                # Ask the user if they want to use the same tracks for the rest of the files
                use_same_tracks = QMessageBox.question(None, "Use Same Tracks", "Do you want to use the same tracks for the rest of the files?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes
            else:
                self.file_tracks[file] = tracks

        self.thread_pool = QThreadPool()
        self.progress_dialog = QProgressDialog("Removing subtitles...", "Cancel", 0, len(self.selected_files))
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)

        for file, tracks in self.file_tracks.items():
            worker = Worker(self.remux_file, file, tracks)
            worker.signals.finished.connect(self.update_progress)
            self.thread_pool.start(worker)




    def remux_file(self, file, tracks):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mkv")
        temp_output_file = temp_file.name
        temp_file.close()

        final_output_file = os.path.join(self.output_folder, os.path.basename(file)) if self.overwrite else self.get_output_filename()

        track_ids = [str(track["id"]) for track in tracks]
        command = f'mkvmerge -o "{temp_output_file}" -s {",".join(track_ids)}'

        for track in tracks:
            if track["is_main"]:
                command += f' --default-track {track["id"]}:yes'

        command += f' "{file}"'
        print(f"{command = }")

        self.run_command(command, temp_output_file, final_output_file)

    def run_command(self, command, temp_output_file, final_output_file):
        os.system(command)
        shutil.move(temp_output_file, final_output_file)

    def get_output_filename(self):
        filename, ok = QInputDialog.getText(None, "Output Filename", "Enter the output filename:")
        if ok and filename:
            return os.path.join(self.output_folder, filename + '.mkv')
        else:
            return None
        
    def get_track_info(self, file):
        tracks = get_subtitle_tracks_ffmpeg(file)
        if tracks:
            dialog = MainTrackSelectionDialog(tracks)
            if dialog.exec():
                selected_tracks = dialog.selected_tracks_info
                self.file_tracks[file] = selected_tracks
                return selected_tracks
    
    def update_progress(self):
        current_value = self.progress_dialog.value()
        self.progress_dialog.setValue(current_value + 1)
                

class WorkerSignals(QObject):
    finished = pyqtSignal()

class Worker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        self.func(*self.args, **self.kwargs)
        self.signals.finished.emit()
