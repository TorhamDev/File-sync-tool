from consts import TELEGRAM_BOT_TOKEN_REGEX
from database.db import get_db
from repositories.telegram import TelegramRepository
from utils.validations import regex_validation

HELP_TEXT = """
insure to have a channel and a bot, and add the bot to your channel as an admin.
get your bot token from @BotFather and your channel id from @username_to_id_bot
"""

def telegram_starter() -> tuple[str, str]:
    print(HELP_TEXT)
    while True:
        bot_token = input("Enter Your Bot Token: ")
        if not regex_validation(pattern=TELEGRAM_BOT_TOKEN_REGEX, string=bot_token):
            continue
        channel_id = input("Enter Your Telegram Channel ID: ")
        break

    repo = TelegramRepository(session=get_db())

    repo.create_telegram_info(token=bot_token, channel_id=channel_id)
    return bot_token, channel_id
