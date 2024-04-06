from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from .callbackdata import MainMenuCB, TrainerOptions, AthletesMenuNavigation

from classes import *


def ikb_main_menu_trainer(trainer: Trainer):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Атлеты', callback_data=AthletesMenuNavigation(button='navigate_athlete'))
    keyboard.button(text='Архив', callback_data=AthletesMenuNavigation(button='navigate_athlete_inactive'))
    keyboard.button(text='Настройки', callback_data=TrainerOptions(button='options',
                                                                   current_show=trainer.options.athletes_show,
                                                                   new_show=0,
                                                                   current_time=trainer.options.schedule_time,
                                                                   new_time=0,
                                                                   refresh=' '))
    return keyboard.as_markup()


def ikb_main_menu_athlete(trainers_list: list[Trainer], current_list_id: int):
    keyboard = InlineKeyboardBuilder()
    return keyboard.as_markup()


def ikb_main_menu_not_user(trainers_list: list[Trainer], current_list_id: int):
    keyboard = InlineKeyboardBuilder()
    return keyboard.as_markup()


# def ikb_main_menu_trainer(trainers_list: list[Trainer], current_list_id: int):
#     keyboard = InlineKeyboardBuilder()
#     if len(trainers_list) > 1:
#         button_prev_trainer(keyboard, (current_list_id - 1) % len(trainers_list))
#         button_select_trainer(keyboard, trainers_list[current_list_id].id)
#         button_next_trainer(keyboard, (current_list_id + 1) % len(trainers_list))
#     else:
#         button_select_trainer(keyboard, trainers_list[current_list_id].id)
#     return keyboard.as_markup()

def button_select_trainer(reply_keyboard: InlineKeyboardBuilder, trainer_id: int):
    reply_keyboard.button(text='Записаться', callback_data=TrainerNavigation(menu='select_trainer',
                                                                             trainer_id=trainer_id))


def button_prev_trainer(reply_keyboard: InlineKeyboardBuilder, prev_list_id: int):
    reply_keyboard.button(text='<<<', callback_data=TrainerNavigation(menu='navi_trainer',
                                                                      trainer_id=prev_list_id))


def button_next_trainer(reply_keyboard: InlineKeyboardBuilder, next_list_id: int):
    reply_keyboard.button(text='>>>', callback_data=TrainerNavigation(menu='navi_trainer',
                                                                      trainer_id=next_list_id))
