from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from .callbackdata import MainMenuCB, VotingNavigationCB, ConfirmCB, TrainerNavigation, TrainerMenu, AthleteCheck

from database import Trainer, Athlete
from .navigation import *

from datetime import date


def ikb_trainer_main_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Атлеты', callback_data=TrainerMenu(menu='AN', current_id=0))
    keyboard.button(text='Архив', callback_data=TrainerMenu(menu='AA', current_id=0))
    keyboard.button(text='Настройки', callback_data=TrainerMenu(menu='TO', current_id=0))
    return keyboard.as_markup()


#
#
# def ikb_athletes_navigation(trainer: Trainer, athlete_list: list[Athlete], current_id: int):
#     keyboard = InlineKeyboardBuilder()
#     interval_size = trainer.options.interval_size
#     athlete_list_interval = athlete_list[current_id * interval_size:current_id * interval_size + interval_size]
#     for index, athlete in enumerate(athlete_list_interval):
#         keyboard.button(text=f'{athlete.last_name} {athlete.first_name}',
#                         callback_data=TrainerMainMenu(menu='AC', current_id=index + interval_size))
#
#     # prev_id = (current_id - 1) % len_list
#     # next_id = (current_id + 1) % len_list
#
#     keyboard.button(text='<<<', callback_data=TrainerMainMenu(menu='AN', current_id=prev_id))
#     keyboard.button(text='Занятие', callback_data=TrainerMainMenu(menu='AN_finish', current_id=current_id))
#     keyboard.button(text='>>>', callback_data=TrainerMainMenu(menu='AN', current_id=next_id))
#     keyboard.button(text='Архив', callback_data=TrainerMainMenu(menu='AA', current_id=current_id))
#     keyboard.button(text='Оплата', callback_data=TrainerMainMenu(menu='AN_pay', current_id=current_id))
#     keyboard.button(text='Главное меню', callback_data=MainMenuCB(menu='MM'))
#     keyboard.adjust(3, 2, 1)
#     return keyboard.as_markup()


def ikb_athletes_navigation_items(current_id: int, athletes_list: list[Athlete], profile: bool, trained: bool):
    keyboard = InlineKeyboardBuilder()
    new_profile = False if profile else True
    add_navigation_button(keyboard, current_id, len(athletes_list), 'AN', items=True)
    if trained:
        keyboard.button(text='Занятие', callback_data=TrainerMenu(menu='AN_finish', current_id=current_id))
    add_navigation_button(keyboard, current_id, len(athletes_list), 'AN', previous=False, items=True)
    keyboard.button(text='Архив' if profile else 'Профиль', callback_data=TrainerMenu(menu='AN',
                                                                                      current_id=current_id,
                                                                                      items=True,
                                                                                      profile=new_profile))
    keyboard.button(text='Оплата', callback_data=TrainerMenu(menu='AN_pay', current_id=current_id))
    keyboard.button(text='Главное меню', callback_data=MainMenuCB(menu='MM'))
    if trained:
        keyboard.adjust(3, 2, 1)
    else:
        keyboard.adjust(2, 2, 1)
    return keyboard.as_markup()


def ikb_athletes_navigation_list(current_list_id: int, athletes_list: list[list[Athlete]]):
    keyboard = InlineKeyboardBuilder()
    for n, athlete in enumerate(athletes_list[current_list_id]):
        cur_id = len(athletes_list[0]) * current_list_id + n
        keyboard.button(text=f'{athlete.first_name} {athlete.last_name}',
                        callback_data=TrainerMenu(menu='AN', current_id=cur_id, items=True))
    add_navigation_button(keyboard, current_list_id, len(athletes_list), 'AN')
    add_navigation_button(keyboard, current_list_id, len(athletes_list), 'AN', previous=False)
    keyboard.button(text='Главное меню', callback_data=MainMenuCB(menu='MM'))
    button_adjust = [1] * len(athletes_list[current_list_id]) + [2, 1]
    keyboard.adjust(*button_adjust)
    return keyboard.as_markup()



