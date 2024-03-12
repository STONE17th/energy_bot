from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from .callbackdata import MainMenuCB, VotingNavigationCB, ConfirmCB, TrainerNavigation

from database import Trainer, Athlete


def ikb_main_menu(trainers_list: list[Trainer], current_list_id: int):
    keyboard = InlineKeyboardBuilder()
    if len(trainers_list) > 1:
        button_prev_trainer(keyboard, (current_list_id - 1) % len(trainers_list))
        button_select_trainer(keyboard, trainers_list[current_list_id].id)
        button_next_trainer(keyboard, (current_list_id + 1) % len(trainers_list))
    else:
        button_select_trainer(keyboard, trainers_list[current_list_id].id)
    return keyboard.as_markup()


# def ikb_request_admin(new_admin_id: int):
#     keyboard = InlineKeyboardBuilder()
#     keyboard.button(text='Принять', callback_data=ConfirmCB(menu='new_admin', button='accept', user_id=new_admin_id))
#     keyboard.button(text='Отмена', callback_data=ConfirmCB(menu='new_admin', button='cancel', user_id=new_admin_id))
#     return keyboard.as_markup()
#
#
# def ikb_back(user_id: int):
#     keyboard = InlineKeyboardBuilder()
#     keyboard.button(text='МЕНЮ', callback_data=MainMenuCB(button='back', user_id=user_id, admin=0))
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
