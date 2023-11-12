from commands.command import Command
from PyQt6.QtWidgets import *
from utils.mkv_utils import get_subtitle_tracks_ffmpeg
from registry.register_command import register_command
from views.track_selection_dialog import TrackSelectionDialog
import subprocess
import os

@register_command("Extract Subtitles")
class ExtractSubtitlesCommand(Command):
    def __init__(self, selected_files):
        self.selected_files = selected_files["mkv"]
        self.files = []

    def execute(self):
        if not self.selected_files:  # Check if the list is empty
            QMessageBox.information(None, "No Files Selected", "No video files have been selected.")
            return
        
        for file in self.selected_files:
            tracks = get_subtitle_tracks_ffmpeg(file)
            if tracks:
                dialog = TrackSelectionDialog(tracks)
                if dialog.exec():
                    selected_tracks = dialog.selected_tracks
                    self.run_extraction(file, selected_tracks)
                    
        self.extract_all(self.ask_for_destination_folder())

    def extract_all(self, destination_folder):
        for file in self.files:
            file, track_id, format, track_info = file
            output_file = self.generate_output_filename(file, track_id, format, track_info, destination_folder)
            self.extract_subtitle(file, track_id, output_file)

    def ask_for_destination_folder(self):
        folder = QFileDialog.getExistingDirectory(None, "Select Destination Folder")
        return folder

    def run_extraction(self, file, selected_tracks):
        for track in selected_tracks:
            track_id, format, track_info = track  # Adjust according to your data structure
            self.files.append((file, track_id, format, track_info))
        
    
    def generate_output_filename(self, file, track_id, format, track_info, destination_folder):
        base_name = os.path.splitext(os.path.basename(file))[0]
        extension = self.determine_extension(format)
        return os.path.join(destination_folder, f"{base_name}_track{track_id}_{track_info.split(' ')[0]}.{extension}")

    def determine_extension(self, format):
        # Map the format to the correct file extension. Adjust as needed.
        format_extension_map = {
            'srt': 'srt',
            'ass': 'ass',
            # Add more mappings for different formats
        }
        return format_extension_map.get(format, 'srt')  # Default to 'srt' if format is unknown

    def extract_subtitle(self, file, track_id, output_file):
        cmd = [
            'ffmpeg',
            '-i', file,
            '-map', f'0:{track_id}',
            '-c:s', 'copy',  # Copy the subtitle as-is without conversion
            output_file
        ]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while extracting subtitles: {e}")