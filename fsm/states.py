from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    name = State()
    phone = State()
    address = State()
    confirm = State()


class NewItemState(StatesGroup):
    type = State()
    name = State()
    description = State()
    price = State()
    count = State()
    confirm = State()


class NewAthleteState(StatesGroup):
    tg_id = State()
    trainer_id = State()
    first_name = State()
    last_name = State()
    photo = State()
    cur_chat = State()
    cur_message = State()
    finish = State()
