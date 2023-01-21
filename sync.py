import json
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


def get_user(user_id) -> str:
    with open('users.json', 'r') as file:
        load = json.load(file)
        user_info = f"Имя: {load[user_id]['name']} \n" \
                    f"Компания: {load[user_id]['company']} \n" \
                    f"Адрес: {load[user_id]['address']} \n" \
                    f"Телефон: {load[user_id]['phone']} \n"
        return user_info



