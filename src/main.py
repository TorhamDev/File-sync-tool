from consts import PlatfromsTypeEnum
from database import get_db
from repositories.base_info import BaseInfoRepository
from utils.factories import get_platfrom_handler
from utils.starters import get_platfrom_starter, select_platfrom

base_info_repo = BaseInfoRepository(session=get_db())


def sync_loop():
    sync_info = base_info_repo.get_last()
    if not sync_info:
        raise ValueError("Can't find any sync info. possible database malfunction.")

    platfrom_handler = get_platfrom_handler(sync_info.sync_type)

    print("Start uploading to telegram.")
    platfrom_handler.upload()


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
