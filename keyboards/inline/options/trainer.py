from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from ..callbackdata import TrainerOptions, MainMenuCB

from classes import *


def ikb_options_trainer(data: TrainerOptions):
    new_refresh = change_refresh(data.refresh)
    keyboard = InlineKeyboardBuilder()
    button_change_value(keyboard, '<<<', current_show=data.current_show,
                        new_show=-1, current_time=data.current_time, new_time=0,
                        refresh=new_refresh)
    keyboard.button(text=f'{data.current_show}',
                    callback_data=TrainerOptions(button='save_show',
                                                 current_show=data.current_show,
                                                 new_show=0,
                                                 current_time=data.current_time,
                                                 new_time=0,
                                                 refresh=new_refresh))
    button_change_value(keyboard, '>>>', current_show=data.current_show,
                        new_show=1, current_time=data.current_time, new_time=0,
                        refresh=new_refresh)
    button_change_value(keyboard, '<<<', current_show=data.current_show,
                        new_show=0, current_time=data.current_time, new_time=-1,
                        refresh=new_refresh)
    keyboard.button(text=f'{data.current_time[:2]}:{data.current_time[2:]}',
                    callback_data=TrainerOptions(button='save_time',
                                                 current_show=data.current_show,
                                                 new_show=0,
                                                 current_time=data.current_time,
                                                 new_time=0,
                                                 refresh=new_refresh))
    button_change_value(keyboard, '>>>', current_show=data.current_show,
                        new_show=0, current_time=data.current_time, new_time=1,
                        refresh=new_refresh)
    keyboard.button(text='Главное меню', callback_data=MainMenuCB(menu='home'))
    keyboard.adjust(3, 3, 1)
    return keyboard.as_markup()


def change_refresh(button: str):
    return ' ' if button == '.' else '.'


def button_select_trainer(reply_keyboard: InlineKeyboardBuilder, trainer_id: int):
    reply_keyboard.button(text='Записаться', callback_data=TrainerNavigation(menu='select_trainer',
                                                                             trainer_id=trainer_id))


def button_change_value(reply_keyboard: InlineKeyboardBuilder,
                        button_text: str,
                        current_show: int = 0, new_show: int = 0,
                        current_time: str = '', new_time: int = 0,
                        refresh: str = '.'):
    reply_keyboard.button(text=button_text, callback_data=TrainerOptions(button='options',
                                                                         current_show=current_show,
                                                                         new_show=new_show,
                                                                         current_time=current_time,
                                                                         new_time=new_time,
                                                                         refresh=refresh))


def change_show(current_value: int, new_value: int):
    return (current_value + new_value) % 6


def change_time(current_value: str, new_value: int):
    if not new_value:
        return current_value
    hours, minutes = list(map(int, [current_value[:2], current_value[2:]]))
    if minutes == 30:
        if new_value > 0:
            return f'{str((hours + 1) % 24).zfill(2)}00'
        return f'{str(hours).zfill(2)}00'
    else:
        if new_value > 0:
            return f'{str(hours).zfill(2)}30'
        return f'{str((hours - 1) % 24).zfill(2)}30'
