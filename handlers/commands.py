from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from database import AthletesDB, Athlete, TrainersDB, Trainer, TrainingsDB, Training

from keyboards.inline.callbackdata import TrainerNavigation
from keyboards import ikb_main_menu, ikb_new_athlete, ikb_trainer_main_menu

import settings
import bot_text

command_router = Router()


@command_router.message(Command('start'))
async def com_start(message: Message, user: Athlete | Trainer | None, bot: Bot):
    print(user)
    trainers_list = [Trainer(item[0]) for item in TrainersDB().load_all()]
    if isinstance(user, Athlete):
        await message.reply('Ты атлет')

        # await bot.send_photo(user.tg_id, photo=user.trainer.photo, caption=str(user.trainer),
        #                      reply_markup=ikb_main_menu(trainers_list, 0))
    elif isinstance(user, Trainer):
        message_text = f'Привет, {user.first_name}! Это твой бот с меню!'
        await bot.send_photo(message.from_user.id, photo=user.photo, caption=message_text,
                             reply_markup=ikb_trainer_main_menu())
    else:
        await bot.send_photo(message.from_user.id, photo=trainers_list[0].photo, caption=str(trainers_list[0]),
                             reply_markup=ikb_main_menu(trainers_list, 0))


@command_router.message(F.photo)
async def get_photo(message: Message):
    print(message.photo[0].file_id)
    await message.answer(message.photo[0].file_id)


@command_router.message(Command('my_id'))
async def get_photo(message: Message):
    print(message.from_user.id)
    await message.answer(str(message.from_user.id))


@command_router.message(Command('athletes'))
async def get_photo(message: Message, user: Trainer):
    data = str([Athlete(user[1]) for user in AthletesDB().for_trainer_by_id(user.id)])
    print(data)
    await message.answer(data)


@command_router.message(Command('admin'))
async def request_admin(message: Message, bot: Bot):
    text_message = f'Пользователь {message.from_user.first_name} ({message.from_user.id}) запрашивает админские права'
    await bot.send_message(settings.SUPER_ADMIN_TG_ID, text_message,
                           reply_markup=ikb_request_admin(message.from_user.id))


@command_router.message(Command('paid'))
async def athlete_paid(message: Message):
    AthletesDB().paid(1)
    await message.reply('Заплатил')


@command_router.message(Command('complete'))
async def athlete_paid(message: Message):
    athlete = Athlete(AthletesDB().load_by_id(1)[1])
    await message.reply(str(Athlete(AthletesDB().load_by_id(1)[1]).first_name))
    if athlete.remain_trainings > 0:
        AthletesDB().complete_session(1)

        await message.reply(f'Позанимался, осталось {Athlete(AthletesDB().load_by_id(1)[1]).remain_trainings} занятий')
    else:
        await message.reply('Кончились занятия')


@command_router.message(Command('arch'))
async def athlete_info(message: Message):
    athlete_id = int(message.text.split()[1])
    result = TrainingsDB().athletes_data(athlete_id)
    await message.reply(str(result))
