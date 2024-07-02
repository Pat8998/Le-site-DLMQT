import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class JSONFileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("caca")
        if event.is_directory:
            return
        else:
            logging.info(f'File modified: {event.src_path}')


# Absolute path to the directory you want to watch
path = os.path.join(os.path.dirname(__file__), 'database')

event_handler = JSONFileEventHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)

try:
    logging.info("Starting observer...")
    observer.start()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Stopping observer...")
    observer.stop()
observer.join()
