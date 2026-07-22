from typing import Callable

from consts import TELEGRAM_BOT_TOKEN_REGEX, PlatfromsTypeEnum
from utils.validations import regex_validation


def telegram_starter() -> tuple[str, str]:
    while True:
        bot_token = input("Enter Your Bot Token: ")
        if not regex_validation(pattern=TELEGRAM_BOT_TOKEN_REGEX, string=bot_token):
            continue
        channel_id = input("Enter Your Telegram Channel ID: ")
        return bot_token, channel_id


def github_start(): ...


def gdrive_starter(): ...


def select_platfrom() -> str:
    print("please select your sync platfrom:")

    platforms = [e.value for e in PlatfromsTypeEnum]

    for number, name in enumerate(platforms):
        print(f"{number}. {name}")

    while True:
        try:
            platfrom = int(input(f"Enter Platfrom Number(0-{len(platforms) - 1}): "))

            return platforms[platfrom]
        except ValueError:
            print(f"Please Enter a valid number (0-{len(platforms) - 1})")
        except IndexError:
            print(f"please select from  (0-{len(platforms) - 1})")


def get_platfrom_starter(name: str) -> Callable:
    platfroms_map = {
        PlatfromsTypeEnum.TELEGRAM.value: telegram_starter,
        PlatfromsTypeEnum.GITHUB.value: github_start,
        PlatfromsTypeEnum.GDRIVE.value: gdrive_starter,
    }

    return platfroms_map[name]
