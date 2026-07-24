from consts import PlatfromsTypeEnum
from database.db import get_db
from platforms.telegram.platform import TelegramPlatfrom
from repositories.base_info import BaseInfoRepository
from repositories.telegram import TelegramRepository


def get_platfrom_handler(platfrom: str):
    print(type(platfrom))
    repo_map = {PlatfromsTypeEnum.TELEGRAM: TelegramRepository(get_db())}
    base_info = BaseInfoRepository(get_db()).get_last()
    platfrom_repo = repo_map[platfrom]
    platfrom_data = platfrom_repo.get_last()

    assert base_info

    if not platfrom_data:
        raise ValueError("No platfrom data been found.")

    platfrom_map = {
        PlatfromsTypeEnum.TELEGRAM: TelegramPlatfrom(
            bot_token=str(platfrom_data.token),
            channel_id=str(platfrom_data.channel_id),
            target_dir=str(base_info.sync_dir),
            backup_temp_dir="/home/torham/Document/",
        )
    }

    return platfrom_map[platfrom]
