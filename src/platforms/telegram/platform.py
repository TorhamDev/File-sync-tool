from platforms.base import BasePlatfrom
from platforms.telegram.uploader import upload_file_to_channel


class TelegramPlatfrom(BasePlatfrom):
    def __init__(
        self,
        bot_token: str,
        channel_id: str,
        target_dir: str,
        backup_temp_dir: str,
    ) -> None:
        super().__init__(target_dir, backup_temp_dir)
        self.bot_token = bot_token
        self.channel_id = channel_id

    def upload(self) -> bool:
        is_success, archive_path = self.compress()

        if is_success:
            upload_file_to_channel(
                file_path=archive_path,
                bot_token=self.bot_token,
                chat_id=self.channel_id,
            )

            return True

        return False

    def fetch(self):
        return super().fetch()

    def last_sync_details(self) -> dict:
        return super().last_sync_details()
