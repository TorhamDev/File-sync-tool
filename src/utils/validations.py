import re


def regex_validation(pattern: str, string: str) -> bool:
    return bool(re.match(pattern=pattern, string=string))
