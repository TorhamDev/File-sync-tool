import re


def regex_validation(pattern: str, string: str) -> bool:
    match = re.match(pattern=pattern, string=string)
    if match:
        return True

    return False
