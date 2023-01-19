from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


def get_main_kb() -> ReplyKeyboardMarkup:
    start_buttons = ['Оформить заказ', 'Регистрация']
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    return keyboard


def get_back_kb() -> InlineKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Главное меню")
    return keyboard


