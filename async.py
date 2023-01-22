from sqlite import start_db, edit_profile, create_user, check_user
from keyboards import get_main_kb, register_check_kb, deliver_kb
from states import RegisterStatesGroup, DeliverStatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from sync import get_user
import json
import os


BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def on_startup(_):
    await start_db()


@dp.message_handler(commands='start')
async def start_func(message: types.Message) -> None:
    await message.answer('Добро пожаловать',
                         reply_markup=get_main_kb())
    await message.delete()


@dp.message_handler(Text(equals="Завершить"),
                    state=RegisterStatesGroup.finish_state)
async def start_func(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        await edit_profile(state=state, user_id=message.from_user.id)
        await state.finish()

    await message.answer(text="Вы вернулись в главное меню",
                            reply_markup=get_main_kb())


@dp.message_handler(Text(equals="Исправить данные"),
                    state=RegisterStatesGroup.finish_state)
async def register_fix(message: types.Message, state: FSMContext) -> None:
    await message.answer("Пожалуйста, введите своё имя:")
    await RegisterStatesGroup.name.set()


@dp.message_handler(Text(equals="Оформить заказ"))
async def make_order(message: types.Message) -> None:
    match check_user(user_id=message.from_user.id):
        case None:
            await message.answer("Вы не прошли регистрацию. "
                         "Пожалуйста, зарегистрируйтесь.")
        case _:
            await message.answer('Вы перешли в оформление доставки.',
                                     reply_markup=deliver_kb())


@dp.message_handler(Text(equals='Регистрация'))
async def make_registration(message: types.Message) -> None:
    await create_user(user_id=message.from_user.id)
    await message.reply("Вы перешли в форму регистрации.",
                        reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Пожалуйста, введите своё имя:")
    await RegisterStatesGroup.name.set()


@dp.message_handler(state=RegisterStatesGroup.name)
async def get_name(message: types.Message,state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply("Пожалуйста, введите название компании:")
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
                         "в формате +375XXXXXXXXX (без +375 и пробела):")
    await RegisterStatesGroup.next()


@dp.message_handler(state=RegisterStatesGroup.phone)
async def get_phone_number(message: types.Message,
                           state: FSMContext) -> None:
    async with state.proxy() as data:
        data["phone"] = f"+375{message.text}"
        await message.answer("Пожалуйста, проверьте правильность "
                             "введенных данных. Если всё верно, "
                             "нажмите кнопку 'Завершить'.\n\n"
                             f"Имя:   {data['name']} \n"
                             f"Компания:   {data['company']}\n"
                             f"Адрес:   {data['address']}\n"
                             f"Телефон:   {data['phone']}",
                             reply_markup=register_check_kb())
        await RegisterStatesGroup.next()


@dp.message_handler(Text(equals="Одна доставка"))
async def make_single_order(message: types.Message) -> None:
    await message.answer("Вы выбрали одну доставку. Пожалуйста, "
                         "введите адрес доставки: ")
    await DeliverStatesGroup.deliver_address.set()


@dp.message_handler(state=DeliverStatesGroup.deliver_address)
async def get_deliver_address(message: types.Message,
                              state: FSMContext) -> None:
    async with state.proxy() as data:
        data['deliver_address'] = message.text
    await message.reply("Пожалуйста, введите ориентировочное время "
                        "готовности заказа в формате 24ч:")
    await DeliverStatesGroup.next()


@dp.message_handler(state=DeliverStatesGroup.getting_time)
async def get_deliver_time(message: types.Message,
                              state: FSMContext) -> None:
    async with state.proxy() as data:
        data['getting_time'] = message.text
    await message.reply("Пожалуйста, напишите комментарии к заказу. "
                        "Если таковых нет, напишите знак '.':")
    await DeliverStatesGroup.next()


@dp.message_handler(state=DeliverStatesGroup.comments)
async def get_deliver_comment(message: types.Message,
                              state: FSMContext) -> None:
    async with state.proxy() as data:
        data['comments'] = message.text
    await message.answer("Пожалуйста, проверьте правильность "
                         "введенных данных. Если всё верно, "
                         "нажмите кнопку 'Завершить'.\n\n"
                         f"Адрес доставки:   {data['deliver_address']} \n"
                         f"Ориентировочное время готовности заказа:   "
                         f"{data['getting_time']}\n"
                         f"Комментарий к заказу:   {data['comments']}\n",
                         reply_markup=register_check_kb())
    await DeliverStatesGroup.next()


@dp.message_handler(Text(equals="Исправить данные"),
                    state=DeliverStatesGroup.finish_state)
async def deliver_fix(message: types.Message, state: FSMContext) -> None:
    await message.answer("Пожалуйста, введите адрес доставки: ")
    await DeliverStatesGroup.deliver_address.set()


@dp.message_handler(Text(equals="Завершить"),
                    state=DeliverStatesGroup.finish_state)
async def start_dack_func(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
       # await edit_profile(state=state, user_id=message.from_user.id)
        await state.finish()

    await message.answer(text="Вы вернулись в главное меню",
                            reply_markup=get_main_kb())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)