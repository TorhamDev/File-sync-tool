import time
from threading import Timer

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
    def __init__(
        self,
        sync_type,
        observer,
        target_dir,
        wait_seconds,
    ) -> None:
        super().__init__()
        self.sync_type = sync_type
        self.observer = observer
        self.target_dir = target_dir
        self.wait_seconds = wait_seconds  # 2 minutes = 120 seconds
        self._timer = None

    def process_event(self, event):
        if event.is_directory:
            return

        # Filter out temp/system files
        if event.src_path.endswith((".tmp", ".db", ".DS_Store", ".git")):
            return

        print(f"Change detected: {event.src_path}. Resetting 2-minute timer...")

        # 1. Cancel the existing timer if a new event arrives before 2 mins pass
        if self._timer:
            self._timer.cancel()

        # 2. Schedule a new timer for 2 minutes from NOW
        self._timer = Timer(
            self.wait_seconds, self.trigger_upload, args=[event.src_path]
        )
        self._timer.start()

    def trigger_upload(self, file_path):
        """Called ONLY after 2 minutes of complete silence."""
        print(
            f"\nNo changes detected for {self.wait_seconds} seconds. Starting upload..."
        )

        # Temporarily unschedule to prevent upload file-reads from triggering the watcher
        self.observer.unschedule_all()

        try:
            upload_handler(self.sync_type, "debounced_modified", file_path)
        finally:
            # Re-enable the listener
            self.observer.schedule(self, path=self.target_dir, recursive=True)
            print("Watcher resumed. Waiting for new changes...\n")

    def on_created(self, event):
        self.process_event(event)

    def on_modified(self, event):
        self.process_event(event)


def sync_loop():
    sync_info = base_info_repo.get_last()
    if not sync_info:
        raise ValueError("Can't find any sync info. Possible database malfunction.")

    target_dir = str(sync_info.sync_dir)
    print(target_dir, ".........")

    observer = Observer()

    # Pass the observer and target_dir into the handler so it can pause/resume
    event_handler = DirectoryHandler(
        sync_type=sync_info.sync_type,
        observer=observer,
        target_dir=target_dir,
        wait_seconds=sync_info.sync_wait_time,
    )

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


if __name__ == "__main__":
    if not base_info_repo.base_info_exists():
        platfrom = select_platfrom()
        platfrom_starter = get_platfrom_starter(platfrom)
        sync_dir = input("Enter Target dir you want to sync: ")
        sync_wait_time = int(input("Enter the frequency of sync(in minutes e.g 20):"))
        base_info = base_info_repo.create_base_info(
            sync_type=PlatfromsTypeEnum(platfrom),
            sync_dir=sync_dir,
            sync_wait_time=sync_wait_time * 60,
        )
        platfrom_starter()

    sync_loop()
