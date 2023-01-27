from datetime import datetime, timedelta
from pytz import timezone


def get_hour() -> int:
    tz = timezone('Europe/Minsk')
    hour = datetime.now(tz).hour
    return hour


def get_day() -> int:
    tz = timezone('Europe/Minsk')
    week_day = datetime.weekday(datetime.now(tz))
    return week_day


def get_schedule_date(days: int) -> datetime.date:
    date = datetime.now() + timedelta(days=days)
    return date.date()


def get_schedule_hours(hours: int) -> datetime.date:
    date = datetime.now() + timedelta(hours=hours)
    return date.date()


