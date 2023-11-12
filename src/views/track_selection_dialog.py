from PyQt6.QtWidgets import *

class TrackSelectionDialog(QDialog):
    def __init__(self, tracks):
        super().__init__()
        self.tracks = tracks
        self.selected_tracks = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Create a checkbox for each track
        self.checkboxes = []
        for track in self.tracks:
            # Unpack the track tuple
            print(f"Track info: {track}")
            track_id, track_format, track_info = track

            track_layout = QHBoxLayout()
            checkbox = QCheckBox(f"Track {track_id}: {track_info} - Format: {track_format}")
            self.checkboxes.append(checkbox)
            track_layout.addWidget(checkbox)


            layout.addLayout(track_layout)

        # OK and Cancel buttons
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

    def exec(self):
        result = super().exec()
        if result:
            self.selected_tracks = [track for checkbox, track in zip(self.checkboxes, self.tracks) if checkbox.isChecked()]
        return result

    @property
    def selected_tracks_info(self):
        return [{'id': track['id'], 'format': track['format']} for track in self.selected_tracks]
    
class MainTrackSelectionDialog(QDialog):
    def __init__(self, tracks):
        super().__init__()
        self.tracks = tracks
        self.selected_tracks = []
        self.main_track = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Create a checkbox and a radio button for each track
        self.checkboxes = []
        self.radio_buttons = []
        for track in self.tracks:
            track_id, track_format, track_info = track

            track_layout = QHBoxLayout()
            checkbox = QCheckBox(f"Track {track_id}: {track_info} - Format: {track_format}")
            radio_button = QRadioButton("Main")
            self.checkboxes.append(checkbox)
            self.radio_buttons.append(radio_button)
            track_layout.addWidget(checkbox)
            track_layout.addWidget(radio_button)

            layout.addLayout(track_layout)

        # OK and Cancel buttons
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

    def exec(self):
        result = super().exec()
        if result:
            self.selected_tracks = [(track, checkbox.isChecked(), radio_button.isChecked()) for checkbox, radio_button, track in zip(self.checkboxes, self.radio_buttons, self.tracks)]
        return result

    @property
    def selected_tracks_info(self):
        return [{'id': track[0], 'format': track[1], 'language': track[2], 'is_main': is_main} for track, is_checked, is_main in self.selected_tracks if is_checked]