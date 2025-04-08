import logging
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=2))  # 'Europe/Zurich'
logging.basicConfig(level=logging.INFO)


class CLRS:
    """
    ANSI escape sequences for colored terminal text.
    """
    # --- set print colors ---
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def ct() -> str:
    """
    :return: current date and time
    """
    return datetime.now().strftime("%d.%m.%Y, %H:%M:%S")


def read_prompt(path: str) -> str:
    """
    :return: read prompt from file
    """
    with open(path, 'r') as f:
        prompt = f.read()
    return prompt
