import os
import shutil
from abc import ABC


class BasePlatfrom(ABC):
    def __init__(self, target_dir: str, backup_temp_dir: str) -> None:
        self.target_dir = target_dir
        self.backup_temp_dir = backup_temp_dir

    def upload(self) -> bool: ...

    def fetch(self): ...

    def last_sync_details(self) -> dict: ...

    def compress(self) -> tuple[bool, str | None]:
        filename = "backup"
        try:
            archive = shutil.make_archive(
                base_name=os.path.join(self.backup_temp_dir, filename),  # Saves it here
                format="zip",
                root_dir=self.target_dir,  # Compresses this
            )
        except FileNotFoundError:
            return (False, None)

        return (True, archive)
