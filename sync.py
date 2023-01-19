from datetime import datetime
from pytz import timezone


def get_hour() -> int:
    tz = timezone('Europe/Minsk')
    hour = datetime.now(tz).hour
    return hour


def get_day() -> int:
    tz = timezone('Europe/Minsk')
    week_day = datetime.weekday(datetime.now(tz))
    return week_day



