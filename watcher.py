import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import subprocess

class Handler(FileSystemEventHandler):
    IGNORE_PATTERNS = [".git", "__pycache__"]

    def on_modified(self, event):
            if any(pattern in event.src_path for pattern in self.IGNORE_PATTERNS):
                return
            
            print(f'File changed: {event.src_path}')
            self.restart()

    def restart(self):
        if hasattr(self, 'process'):
            self.process.kill()
        self.process = subprocess.Popen(['python', 'src/main.py'])

if __name__ == "__main__":
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path='./src', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    #
