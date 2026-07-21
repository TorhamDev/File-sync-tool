from enum import Enum


class PlatfromsTypeEnum(Enum):
    TELEGRAM = "Telegram"
    GITHUB = "Github"
    GDRIVE = "GoogleDrive"


TELEGRAM_BOT_TOKEN_REGEX = r"[0-9]{10}:[A-Za-z0-9_-]{35}"
