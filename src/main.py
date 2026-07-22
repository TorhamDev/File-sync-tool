from database import get_db
from repositories.base_info import BaseInfoRepository
from utils.starters import get_platfrom_starter, select_platfrom

if __name__ == "__main__":
    base_info_repo = BaseInfoRepository(session=get_db())

    if base_info_repo.base_info_exists():
        pass

    else:
        platfrom_starter = get_platfrom_starter(select_platfrom())

        platfrom_starter()
