import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from consts import PlatfromsTypeEnum
from database import get_db
from repositories.base_info import BaseInfoRepository
from utils.factories import get_platfrom_handler
from utils.starters import get_platfrom_starter, select_platfrom

base_info_repo = BaseInfoRepository(session=get_db())


def upload_handler(sync_type, event_type, file_path):

    print(f"Triggered! Action: {event_type} on {file_path}")

    platfrom_handler = get_platfrom_handler(sync_type)

    print("Start uploading to telegram.")
    platfrom_handler.upload()


class DirectoryHandler(FileSystemEventHandler):
    def __init__(self, sync_type) -> None:
        super().__init__()
        self.sync_type = sync_type

    def on_any_event(self, event):
        if event.is_directory:
            return

        upload_handler(self.sync_type, event.event_type, event.src_path)


def sync_loop():
    sync_info = base_info_repo.get_last()
    if not sync_info:
        raise ValueError("Can't find any sync info. possible database malfunction.")

    target_dir = str(sync_info.sync_dir)
    print(target_dir, ".........")

    event_handler = DirectoryHandler(sync_type=sync_info.sync_type)
    observer = Observer()


    observer.schedule(event_handler, path=target_dir, recursive=True)

    print(f"Watching directory: {target_dir}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Stopped watcher.")

    observer.join()


def my_custom_function(event_type, file_path):
    print(f"Triggered! Action: {event_type} on {file_path}")


if __name__ == "__main__":
    if not base_info_repo.base_info_exists():
        platfrom = select_platfrom()
        platfrom_starter = get_platfrom_starter(platfrom)
        sync_dir = input("Enter Target dir you want to sync: ")
        base_info = base_info_repo.create_base_info(
            sync_type=PlatfromsTypeEnum(platfrom),
            sync_dir=sync_dir,
        )
        platfrom_starter()

    sync_loop()
