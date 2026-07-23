from database import get_db
from repositories.base_info import BaseInfoRepository
from utils.starters import get_platfrom_starter, select_platfrom
from consts import PlatfromsTypeEnum

if __name__ == "__main__":
    base_info_repo = BaseInfoRepository(session=get_db())

    if base_info_repo.base_info_exists():
        pass

    else:
        platfrom = select_platfrom()
        platfrom_starter = get_platfrom_starter(platfrom)
        sync_dir = input("Enter Target dir you want to sync: ")
        base_info = base_info_repo.create_base_info(
            sync_type=PlatfromsTypeEnum(platfrom),
            sync_dir=sync_dir,
        )
        platfrom_starter()
