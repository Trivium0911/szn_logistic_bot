from sqlite import start_db, edit_profile, create_user, check_user, \
    edit_deliver, get_user_info, get_statistic
from keyboards import get_main_kb, get_register_check_kb, get_deliver_kb, \
    get_cancel_kb, get_admin_kb, get_stats_kb
from states import RegisterStatesGroup, DeliverStatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from sync import get_hour, get_day
import asyncio
import json
import os


BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
owner_id = (os.getenv('OWNER_ID'), )


async def on_startup(_):
    await start_db()


@dp.message_handler(Text(equals="Отмена"), commands='Отмена')
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cansel_func(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    match current_state:
        case None:
            return
    await state.finish()
    await message.answer('Добро пожаловать',
                         reply_markup=get_main_kb())
    await message.delete()


@dp.message_handler(commands='start')
async def start_func(message: types.Message) -> None:
    match str(message.from_user.id) in owner_id:
        case True:
            await message.answer('Добро пожаловать',
                         reply_markup=get_admin_kb())
        case False:
            await message.answer('Добро пожаловать',
                         reply_markup=get_main_kb())
    await message.delete()


@dp.message_handler(Text(equals="Статистика"))
async def statistic_menu(message: types.Message) -> None:
    await message.answer('Добро пожаловать',
                         reply_markup=get_stats_kb())

@dp.message_handler(Text(equals="Назад"))
async def start_back_to_menu(message: types.Message) -> None:
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
    await RegisterStatesGroup.name.set()
    await message.answer("Пожалуйста, введите своё имя:",
                         reply_markup=get_cancel_kb())



@dp.message_handler(Text(equals="Оформить заказ"))
async def make_order(message: types.Message) -> None:
    match check_user(user_id=message.from_user.id):
        case None:
            await message.answer("Вы не прошли регистрацию. "
                         "Пожалуйста, зарегистрируйтесь.")
        case _:
            await message.answer('Вы перешли в оформление доставки.',
                                     reply_markup=get_deliver_kb())


@dp.message_handler(Text(equals='Регистрация'))
async def make_registration(message: types.Message) -> None:
    await create_user(user_id=message.from_user.id)
    await message.reply("Вы перешли в форму регистрации.",
                        reply_markup=types.ReplyKeyboardRemove())
    await RegisterStatesGroup.name.set()
    await message.answer("Пожалуйста, введите своё имя:",
                         reply_markup=get_cancel_kb())



@dp.message_handler(state=RegisterStatesGroup.name)
async def get_name(message: types.Message,state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text
    await RegisterStatesGroup.next()
    await message.reply("Пожалуйста, введите название компании:",
                         reply_markup=get_cancel_kb())



@dp.message_handler(state=RegisterStatesGroup.company)
async def get_company(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['company'] = message.text
    await RegisterStatesGroup.next()
    await message.reply("Пожалуйста, введите свой адрес компании:",
                         reply_markup=get_cancel_kb())



@dp.message_handler(state=RegisterStatesGroup.address)
async def get_address(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['address'] = message.text
    await RegisterStatesGroup.next()
    await message.reply("Пожалуйста, введите номер телефона для связи"
                         "в формате +375XXXXXXXXX (без +375 и пробела):",
                         reply_markup=get_cancel_kb())



@dp.message_handler(state=RegisterStatesGroup.phone)
async def get_phone_number(message: types.Message,
                           state: FSMContext) -> None:
    async with state.proxy() as data:
        data["phone"] = f"+375{message.text}"
    await RegisterStatesGroup.next()
    await message.answer("Пожалуйста, проверьте правильность "
                             "введенных данных. Если всё верно, "
                             "нажмите кнопку 'Завершить'.\n\n"
                             f"Имя:   {data['name']} \n"
                             f"Компания:   {data['company']}\n"
                             f"Адрес:   {data['address']}\n"
                             f"Телефон:   {data['phone']}",
                             reply_markup=get_register_check_kb())



@dp.message_handler(Text(equals="Сформировать доставку"))
async def make_single_order(message: types.Message) -> None:
    await DeliverStatesGroup.deliver_address.set()
    await message.answer("Пожалуйста, введите адрес доставки. "
                         "Если таковых несколько, введите адрес каждой "
                         "на отдельной строке в одном сообщении: ",
                         reply_markup=get_cancel_kb())



@dp.message_handler(state=DeliverStatesGroup.deliver_address)
async def get_deliver_address(message: types.Message,
                              state: FSMContext) -> None:
    async with state.proxy() as data:
        data['deliver_address'] = message.text
        data['count'] = len(message.text.split('\n'))
    await DeliverStatesGroup.next()
    await message.reply("Пожалуйста, введите ориентировочное время "
                        "готовности заказа в формате 24ч.:",
                         reply_markup=get_cancel_kb())



@dp.message_handler(state=DeliverStatesGroup.getting_time)
async def get_deliver_time(message: types.Message,
                              state: FSMContext) -> None:
    async with state.proxy() as data:
        data['getting_time'] = message.text
    await DeliverStatesGroup.next()
    await message.reply("Пожалуйста, напишите комментарии к заказу. "
                        "Если таковых нет, напишите знак '.':",
                         reply_markup=get_cancel_kb())



@dp.message_handler(state=DeliverStatesGroup.comments)
async def get_deliver_comment(message: types.Message,
                              state: FSMContext) -> None:
    async with state.proxy() as data:
        data['comments'] = message.text
        data['package'] =  f"Адрес(а) доставки(ок):  \n\n" \
                           f"{data['deliver_address']} \n\n" \
                           f"Всего заказов:    {data['count']} \n" \
                           f"Ориентировочное время готовности заказа:   " \
                           f"{data['getting_time']}\n\n" \
                           f"Комментарий к заказу:   {data['comments']}\n"
    await DeliverStatesGroup.next()
    await message.answer("Пожалуйста, проверьте правильность "
                         "введенных данных. Если всё верно, "
                         "нажмите кнопку 'Завершить'.\n\n" + data['package'],
                         reply_markup=get_register_check_kb())



@dp.message_handler(Text(equals="Исправить данные"),
                    state=DeliverStatesGroup.finish_state)
async def deliver_fix(message: types.Message, state: FSMContext) -> None:
    await DeliverStatesGroup.deliver_address.set()
    await message.answer("Пожалуйста, введите адрес доставки: "
                         "Если таковых несколько, введите адрес каждой "
                         "на отдельной строке в одном сообщении: ",
                         reply_markup=get_cancel_kb())



@dp.message_handler(Text(equals="Завершить"),
                    state=DeliverStatesGroup.finish_state)
async def start_back_func(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        hour = get_hour()
        await edit_deliver(state, message.from_user.id, hour)
        await bot.send_message(chat_id=os.getenv('CHAT_ID'),
                text=f"{get_user_info(message.from_user.id)} "
                     f"***{data['package']}***",
                             parse_mode='Markdown')
    await state.finish()
    await message.answer(text="Вы вернулись в главное меню",
                            reply_markup=get_main_kb())


@dp.message_handler(Text(equals="За последний день"))
async def statistic_1_day(message: types.Message) -> None:
    result = get_statistic(1)
    await message.answer(f"Статистика за прошлый день: \n\n"
                         f"{result}",
                         reply_markup=get_admin_kb())


@dp.message_handler(Text(equals="Неделя"))
async def statistic_7_days(message: types.Message) -> None:
    result = get_statistic(7)
    await message.answer(f"Статистика за неделю: \n\n"
                         f"{result}",
                         reply_markup=get_admin_kb())

@dp.message_handler(Text(equals="Месяц"))
async def statistic_month(message: types.Message) -> None:
    result = get_statistic(30)
    await message.answer(f"Статистика за месяц: \n\n"
                         f"{result}",
                         reply_markup=get_admin_kb())

@dp.message_handler(Text(equals="Год"))
async def statistic_year(message: types.Message) -> None:
    result = get_statistic(365)
    await message.answer(f"Статистика за год: \n\n"
                         f"{result}",
                         reply_markup=get_admin_kb())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)