from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from keyboards import get_main_kb, get_back_kb
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import json
import os


BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class RegisterStatesGroup(StatesGroup):

    name = State()
    company = State()
    address = State()
    phone = State()


@dp.message_handler(commands='start')
async def start_func(message: types.Message) -> None:
    await message.answer('Добро пожаловать')

    await message.answer('Что ж, погнали!',
                         reply_markup=get_main_kb())
    await message.delete()


@dp.message_handler(Text(equals="Главное меню"))
async def start_func(message: types.Message) -> None:
    await message.answer(text="Вы вернулись в главное меню",
                            reply_markup=get_main_kb())


@dp.message_handler(Text(equals="Оформить заказ"))
async def make_order(message: types.Message) -> None:
    await message.delete()

    with open("users.json", "r") as file:
        load = json.load(file)
        match str(message.from_user.id) in load:
            case True:
                ...
            case False:
                await message.answer("Вы не прошли регистрацию. "
                                    "Пожалуйста, зарегистрируйтесь.")


@dp.message_handler(Text(equals='Регистрация'))
async def make_registration(message: types.Message) -> None:
    await message.reply("Вы перешли в форму регистрации.",
                        reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Пожалуйста, введите своё имя:")
    await RegisterStatesGroup.name.set()


@dp.message_handler(state=RegisterStatesGroup.name)
async def get_name(message: types.Message,state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply("Пожалуйста, введите название организации:")
    await RegisterStatesGroup.next()


@dp.message_handler(state=RegisterStatesGroup.company)
async def get_company(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['company'] = message.text
    await message.reply("Пожалуйста, введите свой адрес компании:")
    await RegisterStatesGroup.next()


@dp.message_handler(state=RegisterStatesGroup.address)
async def get_address(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['address'] = message.text
    await message.reply("Пожалуйста, введите номер телефона для связи"
                         "в формате +375XXXXXXXXX (без +375):")
    await RegisterStatesGroup.next()


@dp.message_handler(state=RegisterStatesGroup.phone)
async def get_phone_number(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["phone"] = f"+375{message.text}"
        with open('users.json', 'r') as file:
            load = json.load(file)
            load.update(
                {
                    f"{message.from_user.id}":
                    {
                        "name": data["name"],
                        "company": data["company"],
                        "address": data["address"],
                        "phone": data["phone"]
                    }
                }
            )
            with open('users.json', 'w') as file:
                json.dump(load, file, indent=4, ensure_ascii=False)
    await state.finish()
    await message.answer("Вы успешно прошли регистрацию."
                         "Для возврата в главное меню нажмите кнопку"
                         "'Главное меню'",
                         reply_markup=get_back_kb())



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)