import shutil
from datetime import date
from pathlib import Path

from watchdog.events import FileSystemEventHandler

from desktop_cleaner.extensions import extension_paths


def add_paths(path: Path):
    dated_path = path / f'{date.today().year}' / f'{date.today().month:02d}'
    dated_path.mkdir(parents=True, exist_ok=True)
    return dated_path


def rename_file(source: Path, dir_path: Path):
   
    if Path(dir_path / source.name).exists():
        increment = 0

        while True:
            increment += 1
            new_name = dir_path / f'{source.stem}_{increment}{source.suffix}'

            if not new_name.exists():
                return new_name
    else:
        return dir_path/source.name


class EventHandler(FileSystemEventHandler):
    def __init__(self, watch_path: Path, destination_root: Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

    def on_modified(self, event):
        for child in self.watch_path.iterdir():
            if child.is_file() and child.suffix.lower() in extension_paths:
                dir_path = self.destination_root / extension_paths[child.suffix.lower()]
                dir_path = add_paths(path=dir_path)
                dir_path = rename_file(source=child, dir_path=dir_path)
                shutil.move(src=child, dst=dir_path)
