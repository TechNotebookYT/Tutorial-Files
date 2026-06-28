#!/usr/bin/env python3
"""
watcher.py
Watches the Screenshots folder for new .png files, tags them with the local
vision model, and renames them to YYYY-MM-DD_HH-MM-SS_<tag>.png.
Run: uv run watcher.py
"""

import os
import re
import time
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from renamer import tag_screenshot

WATCH_DIR = "" # Insert Directory name here 
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rename.log")
SETTLE_SECONDS = 2

# Matches files this watcher has already renamed: YYYY-MM-DD_HH-MM-SS_<tag>.png
RENAMED_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_.+\.png$")


def log(message: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')}  {message}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def process(path: str) -> None:
    filename = os.path.basename(path)

    if RENAMED_PATTERN.match(filename):
        return  # already renamed by us

    if not os.path.exists(path):
        return  # moved/deleted before we got to it

    try:
        tag = tag_screenshot(path)
    except Exception as e:
        log(f"ERROR tagging {filename}: {e}")
        return

    if not tag:
        log(f"SKIP {filename}: empty tag")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_name = f"{timestamp}_{tag}.png"
    new_path = os.path.join(os.path.dirname(path), new_name)

    try:
        os.rename(path, new_path)
    except OSError as e:
        log(f"ERROR renaming {filename}: {e}")
        return

    log(f"RENAMED {filename} -> {new_name}")


class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if not event.src_path.lower().endswith(".png"):
            return
        time.sleep(SETTLE_SECONDS)  # let the file finish writing
        process(event.src_path)


def main():
    if not os.path.isdir(WATCH_DIR):
        raise SystemExit(f"Watch directory does not exist: {WATCH_DIR}")

    observer = Observer()
    observer.schedule(ScreenshotHandler(), WATCH_DIR, recursive=False)
    observer.start()
    log(f"Watching {WATCH_DIR} for new screenshots...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("Stopping watcher.")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
