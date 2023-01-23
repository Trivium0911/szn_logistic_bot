from aiogram.types import ReplyKeyboardMarkup


def get_main_kb() -> ReplyKeyboardMarkup:
    start_buttons = ['Регистрация', 'Оформить заказ']
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    return keyboard


def register_check_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Исправить данные", "Завершить")
    return keyboard


def deliver_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Сформировать доставку").add("Назад")
    return keyboard


def cancel_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Отмена')
    return keyboard
