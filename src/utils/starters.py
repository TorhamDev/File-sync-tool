from typing import Callable

from consts import PlatfromsTypeEnum
from platforms.gdrive import gdrive_starter
from platforms.github import github_starter
from platforms.telegram import telegram_starter


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
        PlatfromsTypeEnum.GITHUB.value: github_starter,
        PlatfromsTypeEnum.GDRIVE.value: gdrive_starter,
    }

    return platfroms_map[name]
