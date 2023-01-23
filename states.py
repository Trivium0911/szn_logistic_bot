from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterStatesGroup(StatesGroup):

    name = State()
    company = State()
    address = State()
    phone = State()
    finish_state = State()


class DeliverStatesGroup(StatesGroup):

    deliver_address = State()
    getting_time = State()
    comments = State()
    finish_state = State()


