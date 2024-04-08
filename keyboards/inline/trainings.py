from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from .callbackdata import MainMenuCB, ConfirmCB, TrainerMenu, AthleteCheck

from classes import *
from .navigation import *

from database import TrainingsDB


def ikb_athletes_list(trainer: Trainer):
    athletes_list = sorted(
        [Athlete(athlete_id[0], tg_id=False) for athlete_id in TrainingsDB().not_training_today(trainer.id)],
        key=lambda x: f'{x.first_name} {x.last_name}')
    keyboard = InlineKeyboardBuilder()
    for athlete in athletes_list:
        keyboard.button(text=f'{athlete.first_name} {athlete.last_name}',
                        callback_data=AthleteCheck(button='add_today_training', athlete_id=athlete.id))
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()
