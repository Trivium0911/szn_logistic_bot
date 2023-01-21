from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


def get_main_kb() -> ReplyKeyboardMarkup:
    start_buttons = ['Оформить заказ', 'Регистрация']
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    return keyboard


def register_check_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Исправить данные", "Завершить")
    return keyboard



