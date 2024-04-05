from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from .callbackdata import MainMenuCB, VotingNavigationCB, ConfirmCB, TrainerNavigation, TrainerMenu, AthleteCheck

from database import Trainer, Athlete, AthletesDB
from .navigation import *

from datetime import date


def ikb_athletes_list(trainer: Trainer):
    today = date.today()
    athletes_list = sorted(AthletesDB().today_not_training(trainer.id, str(today)), key=lambda x: x.first_name)
    keyboard = InlineKeyboardBuilder()
    for athlete in athletes_list:
        keyboard.button(text=f'{athlete.first_name} {athlete.last_name}',
                        callback_data=AthleteCheck(menu='AtCh', trainer_id=trainer.tg_id, athlete_id=athlete.id))
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()
