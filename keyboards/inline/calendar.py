from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from .callbackdata import AthletesMenuNavigation, TrainingCalendar

from classes import *


def ikb_calendar(athlete: Athlete, callback_data: TrainingCalendar, training_view: bool, active):
    training_list = sorted(athlete.calendar)
    cur_month = callback_data.current_month
    month_calendar = athlete.calendar[training_list[cur_month]].days
    keyboard = InlineKeyboardBuilder()
    if len(training_list) > 1:
        keyboard.button(text='<<<', callback_data=TrainingCalendar(button='calendar' if active else 'calendar_inactive',
                                                                   athlete_id=callback_data.athlete_id,
                                                                   view=callback_data.view,
                                                                   current_month=(cur_month - 1) % len(training_list)))

    button_text = 'Платежи' if callback_data.view == 'Training' else 'Тренировки'
    callback_view = 'Payment' if callback_data.view == 'Training' else 'Training'

    keyboard.button(text=button_text,
                    callback_data=TrainingCalendar(button='calendar' if active else 'calendar_inactive',
                                                   athlete_id=callback_data.athlete_id,
                                                   current_month=cur_month,
                                                   view=callback_view))
    if len(training_list) > 1:
        keyboard.button(text='>>>', callback_data=TrainingCalendar(button='calendar' if active else 'calendar_inactive',
                                                                   athlete_id=callback_data.athlete_id,
                                                                   view=callback_data.view,
                                                                   current_month=(cur_month + 1) % len(training_list)))
    # training = None
    for day in month_calendar:
        training = ('✅' if day.training else None) if callback_data.view == 'Training' else (
            f'{day.payment}💰' if day.payment else None)
        button = training if training else (str(day.number) if day.number else ' ')
        year_month_day = f'{training_list[cur_month]}-{str(day.number).zfill(2)}'
        action = ('remove' if active else 'remove_inactive') if training else ('add' if active else 'add_inactive')
        keyboard.button(text=button, callback_data=TrainingCalendar(button=action if day.number else 'None',
                                                                    athlete_id=callback_data.athlete_id,
                                                                    target_date=year_month_day,
                                                                    current_month=callback_data.current_month))

    # for weekday in training_days:
    #     for day in weekday:
    #         if isinstance(day, int):
    #             date = f'{training_list[cur_month]}-{str(day).zfill(2)}'
    #             day = str(day) if day else ' '
    #             action = 'add' if active else 'add_inactive'
    #
    #         else:
    #             date = f'{training_list[cur_month]}-{str(day.split("_")[0]).zfill(2)}'
    #             day = day.split('_')[1] if day else ' '
    #             action = 'remove' if active else 'remove_inactive'
    #         keyboard.button(text=day,
    #                         callback_data=TrainingCalendar(button=action,
    #                                                        athlete_id=callback_data.athlete_id,
    #                                                        target_date=date,
    #                                                        current_month=callback_data.current_month))
    keyboard.button(text='Назад',
                    callback_data=AthletesMenuNavigation(
                        button='select_athlete' if active else 'select_athlete_inactive',
                        athlete_id=callback_data.athlete_id))
    keyboard.adjust(3 if len(training_list) > 1 else 1, *[7] * (len(month_calendar) // 7), 1)

    return keyboard.as_markup()
