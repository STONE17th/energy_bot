from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from .callbackdata import MainMenuCB, AthletesMenuNavigation, TrainingCalendar, AthletePayment

from classes import *
from .navigation import *

from datetime import date


def ikb_athletes_navigation(trainer: Trainer, callback_data: AthletesMenuNavigation, active: bool):
    athletes_list = sorted(trainer.athletes_active if active else trainer.athletes_inactive, key=lambda x: x.first_name)
    shift = int(trainer.options.athletes_show)
    keyboard = InlineKeyboardBuilder()
    map_kb = []
    for i in range(callback_data.list_id * shift, callback_data.list_id * shift + shift):
        if i >= len(athletes_list):
            break
        name = f'{athletes_list[i].first_name} {athletes_list[i].last_name}'
        keyboard.button(text=name,
                        callback_data=AthletesMenuNavigation(
                            button='select_athlete' if active else 'select_athlete_inactive',
                            athlete_id=i))
        map_kb.append(1)
    if len(athletes_list) > shift:
        len_list = (len(athletes_list) // shift + bool(len(athletes_list) % shift))
        add_navigation_button(keyboard, '<<<', 'navigate_athlete' if active else 'navigate_athlete_inactive',
                              list_id=(callback_data.list_id - 1) % len_list)
        add_navigation_button(keyboard, '>>>', 'navigate_athlete' if active else 'navigate_athlete_inactive',
                              list_id=(callback_data.list_id + 1) % len_list)
        map_kb.append(2)
    keyboard.button(text='Главное меню', callback_data=MainMenuCB(menu='home'))
    keyboard.adjust(*map_kb, 1)
    return keyboard.as_markup()


def ikb_athletes_profile_navigation(trainer: Trainer, callback_data: AthletesMenuNavigation, active: bool):
    athletes_list = sorted(trainer.athletes_active if active else trainer.athletes_inactive, key=lambda x: x.first_name)
    # current_athlete = athletes_list[callback_data.athlete_id]
    # shift = int(trainer.options.athletes_show)
    keyboard = InlineKeyboardBuilder()
    map_kb = []
    if athletes_list:
        if len(athletes_list) > 1:
            add_navigation_button(keyboard, '<<<', 'select_athlete' if active else 'select_athlete_inactive',
                                  athlete_id=(callback_data.athlete_id - 1) % len(athletes_list))
            add_navigation_button(keyboard, '>>>', 'select_athlete' if active else 'select_athlete_inactive',
                                  athlete_id=(callback_data.athlete_id + 1) % len(athletes_list))
            map_kb.append(2)
        keyboard.button(text='График',
                        callback_data=TrainingCalendar(button='calendar' if active else 'calendar_inactive',
                                                       athlete_id=callback_data.athlete_id,
                                                       current_month=-1))
        keyboard.button(text='Оплата',
                        callback_data=AthletePayment(button='pay_request' if active else 'pay_request_inactive',
                                                     athlete_id=callback_data.athlete_id,
                                                     pay_amount=12))
    keyboard.button(text='Назад', callback_data=AthletesMenuNavigation(
        button='navigate_athlete' if active else 'navigate_athlete_inactive',
        list_id=0))
    keyboard.adjust(*map_kb, 2, 1)
    return keyboard.as_markup()


def add_navigation_button(ikb: InlineKeyboardBuilder,
                          button_text: str, button_cb: str,
                          list_id: int = 0, athlete_id: int = 0):
    ikb.button(text=button_text, callback_data=AthletesMenuNavigation(button=button_cb,
                                                                      list_id=list_id, athlete_id=athlete_id))


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
