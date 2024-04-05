from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callbackdata import TrainerMenu


def add_navigation_button(keyboard: InlineKeyboardBuilder,
                          current_id: int, list_size: int, menu: str,
                          previous: bool = True, items: bool = False):
    new_id = (current_id + (-1 if previous else 1)) % list_size
    keyboard.button(text='<<<' if previous else '>>>', callback_data=TrainerMenu(menu=menu,
                                                                                 current_id=new_id,
                                                                                 current_list_id=new_id,
                                                                                 items=items))
