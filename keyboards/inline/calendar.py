from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from .callbackdata import AthletesMenuNavigation, TrainingCalendar

from classes import *


def ikb_calendar(trainer: Trainer, athlete: Athlete, callback_data: TrainingCalendar, active):
    training_list = sorted(athlete.calendar)
    cur_month = callback_data.current_month
    training_days = athlete.calendar[training_list[cur_month]].trainings_days
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='<<<', callback_data=TrainingCalendar(button='calendar',
                                                               athlete_id=callback_data.athlete_id,
                                                               current_month=(cur_month - 1) % len(training_list)))
    keyboard.button(text='>>>', callback_data=TrainingCalendar(button='calendar',
                                                               athlete_id=callback_data.athlete_id,
                                                               current_month=(cur_month + 1) % len(training_list)))
    for weekday in training_days:
        for day in weekday:
            if isinstance(day, int):
                date = f'{training_list[cur_month]}-{str(day).zfill(2)}'
                day = str(day) if day else ' '
                action = 'add' if active else 'add_inactive'

            else:
                date = f'{training_list[cur_month]}-{str(day.split("_")[0]).zfill(2)}'
                day = day.split('_')[1] if day else ' '
                action = 'remove' if active else 'remove_inactive'
            keyboard.button(text=day,
                            callback_data=TrainingCalendar(button=action,
                                                           athlete_id=callback_data.athlete_id,
                                                           target_date=date,
                                                           current_month=callback_data.current_month))
    keyboard.button(text='Назад',
                    callback_data=AthletesMenuNavigation(
                        button='select_athlete' if active else 'select_athlete_inactive',
                        athlete_id=callback_data.athlete_id))
    keyboard.adjust(2, *map(len, training_days), 1)
    return keyboard.as_markup()
