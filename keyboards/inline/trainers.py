from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from .callbackdata import MainMenuCB, VotingNavigationCB, ConfirmCB, TrainerNavigation, TrainerMainMenu

from database import Trainer, Athlete


def ikb_trainer_main_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Атлеты', callback_data=TrainerMainMenu(menu='AN', current_id=0))
    keyboard.button(text='Архив', callback_data=TrainerMainMenu(menu='AA', current_id=0))
    keyboard.button(text='Настройки', callback_data=TrainerMainMenu(menu='TO', current_id=0))
    return keyboard.as_markup()


def ikb_athletes_navigation(trainer: Trainer, athlete_list: list[Athlete], current_id: int):
    keyboard = InlineKeyboardBuilder()
    interval_size = trainer.options.interval_size
    athlete_list_interval = athlete_list[current_id * interval_size:current_id * interval_size + interval_size]
    for index, athlete in enumerate(athlete_list_interval):
        keyboard.button(text=f'{athlete.last_name} {athlete.first_name}',
                        callback_data=TrainerMainMenu(menu='AC', current_id=index + interval_size))

    prev_id = (current_id - 1) % len_list
    next_id = (current_id + 1) % len_list

    keyboard.button(text='<<<', callback_data=TrainerMainMenu(menu='AN', current_id=prev_id))
    keyboard.button(text='Занятие', callback_data=TrainerMainMenu(menu='AN_finish', current_id=current_id))
    keyboard.button(text='>>>', callback_data=TrainerMainMenu(menu='AN', current_id=next_id))
    keyboard.button(text='Архив', callback_data=TrainerMainMenu(menu='AA', current_id=current_id))
    keyboard.button(text='Оплата', callback_data=TrainerMainMenu(menu='AN_pay', current_id=current_id))
    keyboard.button(text='Главное меню', callback_data=MainMenuCB(menu='MM'))
    keyboard.adjust(3, 2, 1)
    return keyboard.as_markup()


def ikb_athletes_card(trainer: Trainer, len_list: int, current_id: int):
    keyboard = InlineKeyboardBuilder()
    if trainer.options.athletes_show:
        prev_id = (current_id - 1) % len_list
        next_id = (current_id + 1) % len_list
    else:
        pass
    keyboard.button(text='<<<', callback_data=TrainerMainMenu(menu='AN', current_id=prev_id))
    keyboard.button(text='Занятие', callback_data=TrainerMainMenu(menu='AN_finish', current_id=current_id))
    keyboard.button(text='>>>', callback_data=TrainerMainMenu(menu='AN', current_id=next_id))
    keyboard.button(text='Архив', callback_data=TrainerMainMenu(menu='AA', current_id=current_id))
    keyboard.button(text='Оплата', callback_data=TrainerMainMenu(menu='AN_pay', current_id=current_id))
    keyboard.button(text='Главное меню', callback_data=MainMenuCB(menu='MM'))
    keyboard.adjust(3, 2, 1)
    return keyboard.as_markup()
