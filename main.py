import os
import re
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from langdetect import detect
import json
from pprint import pprint

# /media/apollo/Crucial X62/Anime/Shingeki no Kyojin/Season 4/[Erai-raws] Shingeki no Kyojin - The Final Season - 01 ~ 16 [1080p][Multiple Subtitle]
# Function to clean and extract dialogue from ASS subtitles
def clean_ass_subtitles(text):
    dialogue_lines = [line for line in text.split('\n') if line.startswith('Dialogue:')]
    cleaned_text = ' '.join(re.sub(r'{.*?}', '', line.split(',', 9)[-1]).strip() for line in dialogue_lines)
    return cleaned_text

# Function to extract and analyze a subtitle sample for language detection
def extract_subtitle_sample(mkv_file, track_id):
    temp_output = "temp_subtitle.ass"
    try:
        subprocess.run(["ffmpeg", "-i", mkv_file, "-map", f"0:{track_id}", "-c", "copy", "-t", "30", temp_output], check=True)
        with open(temp_output, 'r') as file:
            sample_text = clean_ass_subtitles(file.read())
        detected_lang = detect(sample_text)
        return detected_lang
    except Exception as e:
        print(f"Error extracting or detecting language: {e}")
        return "Unknown"
    finally:    
        if os.path.exists(temp_output):
            os.remove(temp_output)

# Function to get subtitle tracks from an MKV file using ffprobe
def get_subtitle_tracks_ffmpeg(mkv_file):
    command = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "s",  # Select only subtitle streams
        "-show_entries", "stream",  # Show all entries for each stream
        "-of", "json",  # Output in JSON format
        mkv_file
    ]
    try:
        print("Running command:", " ".join(command))  # Debugging line to show the command
        result = subprocess.run(command, capture_output=True, text=True)
        # Parse the JSON output
        streams_info = json.loads(result.stdout)
        pprint(streams_info)  # Debugging line to print the parsed JSON

        tracks = []
        for stream in streams_info.get('streams', []):
            # Get the track index
            track_id = str(stream.get('index'))
            # Try to get the language from the tags, fall back to 'Unknown' if not present
            track_lang = stream.get('tags', {}).get('language', 'Unknown')
            # Try to get the title from the tags, could contain the language
            track_title = stream.get('tags', {}).get('title', 'No title available')
            # Combine language and title for more complete information
            track_info = f"Language: {track_lang}"
            if track_title != 'No title available':
                track_info += f", Title: {track_title}"
            tracks.append((track_id, track_info))

        return tracks
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
    except subprocess.CalledProcessError as e:
        print(f"ffprobe command failed with error: {e.stderr}")  # Debugging line to show the error message
        return []






# Function to check if language detection is needed and perform it if necessary
def get_subtitle_tracks(mkv_file):
    print(f"Getting subtitle tracks for: {mkv_file}")
    tracks = get_subtitle_tracks_ffmpeg(mkv_file)
    final_tracks = []
    for track_id, track_lang in tracks:
        if track_lang == 'Unknown' or track_lang == 'und':
            calculated_lang = extract_subtitle_sample(mkv_file, track_id)
            final_tracks.append(f"Track {track_id} - Language: {calculated_lang} (calculated)")
        else:
            final_tracks.append(f"Track {track_id} - Language: {track_lang}")
    return final_tracks

# Dialog for selecting subtitle tracks
class SubtitleSelectionDialog(QDialog):
    def __init__(self, tracks, parent=None):
        super(SubtitleSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Subtitle Tracks")

        layout = QVBoxLayout(self)

        self.checkboxes = []
        self.main_track_radiobuttons = []
        for track in tracks:
            hbox = QHBoxLayout()
            cb = QCheckBox(track)
            hbox.addWidget(cb)
            rb = QRadioButton("Set as Main")
            hbox.addWidget(rb)
            layout.addLayout(hbox)
            self.checkboxes.append(cb)
            self.main_track_radiobuttons.append(rb)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

    def selected_tracks(self):
        selected = [cb.isChecked() for cb in self.checkboxes]
        main_track = [rb.isChecked() for rb in self.main_track_radiobuttons]
        return selected, main_track

# Main Application Window
class SubtitleManager(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Subtitle Manager')
        layout = QVBoxLayout()

        self.dirLabel = QLabel('Select a directory containing MKV files:')
        layout.addWidget(self.dirLabel)

        self.dirButton = QPushButton('Select Directory', self)
        self.dirButton.clicked.connect(self.selectDirectory)
        layout.addWidget(self.dirButton)

        self.fileList = QListWidget(self)
        layout.addWidget(self.fileList)

        self.processButton = QPushButton('Process Files', self)
        self.processButton.clicked.connect(self.processFiles)
        layout.addWidget(self.processButton)

        self.setLayout(layout)

    def selectDirectory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.loadFiles(dir_path)

    def loadFiles(self, dir_path):
        self.fileList.clear()
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".mkv"):
                    full_path = os.path.join(root, file)
                    item = QListWidgetItem(full_path)
                    self.fileList.addItem(item)

    def processFiles(self):
        for index in range(self.fileList.count()):
            item = self.fileList.item(index)
            mkv_file = item.text()
            tracks = get_subtitle_tracks(mkv_file)

            dialog = SubtitleSelectionDialog(tracks, self)
            if dialog.exec_():
                selected, main_track = dialog.selected_tracks()
                print(f"Selected tracks for {mkv_file}: {selected}")
                print(f"Main track for {mkv_file}: {main_track}")
                # Implement the actual subtitle modification logic here

if __name__ == '__main__':
    app = QApplication([])
    ex = SubtitleManager()
    ex.show()
    app.exec_()
