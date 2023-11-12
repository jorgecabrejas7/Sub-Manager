import unittest
from unittest.mock import patch, MagicMock
from src.commands.remove_subtitles_command import RemoveSubtitlesCommand
from PyQt6.QtWidgets import QApplication

app = QApplication([])
class TestRemoveSubtitlesCommand(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.selected_files = {"mkv": ["/path/to/file1.mkv", "/path/to/file2.mkv"]}
        self.command = RemoveSubtitlesCommand(self.selected_files)

    def test_execute_no_files_selected(self):
        self.command.selected_files = []
        with patch('src.commands.remove_subtitles_command.QMessageBox') as mock_message_box:
            self.command.execute()
            mock_message_box.information.assert_called_once_with(None, "No Files Selected", "No video files have been selected.")

    def test_execute_overwrite_files_yes(self):
        with patch('src.commands.remove_subtitles_command.QMessageBox') as mock_message_box:
            mock_message_box.question.return_value = mock_message_box.StandardButton.Yes
            self.command.execute()
            self.assertTrue(self.command.overwrite)

    def test_execute_overwrite_files_no(self):
        with patch('src.commands.remove_subtitles_command.QMessageBox') as mock_message_box:
            mock_message_box.question.return_value = MagicMock(button=mock_message_box.Standardbutton.No)
            self.command.execute()
            self.assertFalse(self.command.overwrite)

    def test_execute_get_output_folder(self):
        with patch('src.commands.remove_subtitles_command.QFileDialog') as mock_file_dialog:
            self.command.execute()
            mock_file_dialog.getExistingDirectory.assert_called_once_with(None, "Select Output Folder")

    def test_execute_use_same_tracks(self):
        with patch('src.commands.remove_subtitles_command.QMessageBox') as mock_message_box:
            mock_message_box.question.return_value = MagicMock(button=mock_message_box.Yes)
            with patch.object(self.command, 'get_track_info') as mock_get_track_info:
                self.command.execute()
                self.assertEqual(mock_get_track_info.call_count, 2)

    def test_execute_use_different_tracks(self):
        with patch('src.commands.remove_subtitles_command.QMessageBox') as mock_message_box:
            mock_message_box.question.return_value = MagicMock(button=mock_message_box.No)
            with patch.object(self.command, 'get_track_info') as mock_get_track_info:
                self.command.execute()
                self.assertEqual(mock_get_track_info.call_count, 2)

    def test_get_output_filename(self):
        self.command.output_folder = "/path/to"
        with patch('src.commands.remove_subtitles_command.QInputDialog') as mock_input_dialog:
            mock_input_dialog.getText.return_value = ("output", True)
            self.assertEqual(self.command.get_output_filename(), "/path/to/output.mkv")

    def test_get_track_info(self):
        with patch('src.commands.remove_subtitles_command.get_subtitle_tracks_ffmpeg') as mock_get_subtitle_tracks_ffmpeg:
            mock_get_subtitle_tracks_ffmpeg.return_value = [{"id": 1, "language": "eng", "is_main": True}, {"id": 2, "language": "spa", "is_main": False}]
            with patch('src.commands.remove_subtitles_command.MainTrackSelectionDialog') as mock_dialog:
                mock_dialog.return_value.exec.return_value = True
                mock_dialog.return_value.selected_tracks_info = [{"id": 1, "language": "eng", "is_main": True}]
                self.assertEqual(self.command.get_track_info("/path/to/file1.mkv"), [{"id": 1, "language": "eng", "is_main": True}])

if __name__ == "__main__":
    unittest.main()