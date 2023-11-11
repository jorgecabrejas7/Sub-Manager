from commands.command import Command
from PyQt6.QtWidgets import *
from utils.mkv_utils import get_subtitle_tracks_ffmpeg
from registry.register_command import register_command
from views.track_selection_dialog import TrackSelectionDialog

@register_command("Extract kaka")
class ExtractSubtitlesCommand(Command):
    def __init__(self, selected_files):
        self.selected_files = selected_files["mkv"]

    def execute(self):
        for file in self.selected_files:
            tracks = get_subtitle_tracks_ffmpeg(file)
            if tracks:
                dialog = TrackSelectionDialog(tracks)
                if dialog.exec():
                    selected_tracks = dialog.selected_tracks
                    self.run_extraction(file, selected_tracks)
        
       

