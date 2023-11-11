import subprocess
import json

def get_subtitle_tracks_ffmpeg(mkv_file):
    command = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "s",  # Select only subtitle streams
        "-show_entries", "stream",  # Show all entries for each stream
        "-of", "json",  # Output in JSON format
        str(mkv_file)  # Ensure the file path is a string
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    try:
        streams_info = json.loads(result.stdout)

        
        tracks = []
        for stream in streams_info.get('streams', []):
            track_id = stream.get('index')
            track_format = stream.get('codec_name', 'unknown')  # Get the format
            track_lang = stream.get('tags', {}).get('language', 'und')
            track_title = stream.get('tags', {}).get('title', '')

            track_info = f"{track_title} ({track_lang})"
            if track_lang == 'und' and not track_title:
                track_info = 'Unknown'

            tracks.append((track_id, track_format, track_info))  # Include format

        return tracks
    except json.JSONDecodeError:
        print("Error parsing JSON from ffprobe output")
        return []
