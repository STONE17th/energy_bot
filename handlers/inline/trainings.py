from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto

from classes import *
from database import AthletesDB

from handlers.inline.main_menu import callback_main_menu

from keyboards.inline.callbackdata import TrainingCalendar
from keyboards import ikb_calendar

from datetime import date

trainings_router = Router()

rus_month = ['январь', 'февраль', 'март', 'апрель',
             'май', 'июнь', 'июль', 'август',
             'сентябрь', 'октябрь', 'ноябрь', 'декабрь']


@trainings_router.callback_query(TrainingCalendar.filter(F.button.in_({'calendar', 'calendar_inactive'})))
async def training_calendar(callback: CallbackQuery, callback_data: TrainingCalendar, user: Trainer, bot: Bot):
    switch = True if callback_data.button == 'calendar' else False
    athletes_list = sorted(user.athletes_active if switch else user.athletes_inactive, key=lambda x: x.first_name)
    current_athlete = athletes_list[callback_data.athlete_id]
    current_month = callback_data.current_month
    month_list = [f'2024-{str(month).zfill(2)}' for month in range(1, date.today().month + 1)]
    cur_year, cur_month = list(map(int, month_list[current_month].split('-')))
    message_text = f'Атлет: {current_athlete.first_name} {current_athlete.last_name}\n'
    message_text += f'Тренировки за {rus_month[cur_month - 1].title()} {cur_year}'
    message_media = InputMediaPhoto(media=current_athlete.photo, caption=message_text)
    await bot.edit_message_media(media=message_media, chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id,
                                 reply_markup=ikb_calendar(user, current_athlete, callback_data, switch))


@trainings_router.callback_query(
    TrainingCalendar.filter(F.button.in_({'remove', 'add', 'remove_inactive', 'add_inactive'})))
async def training_calendar(callback: CallbackQuery, callback_data: TrainingCalendar, user: Trainer, bot: Bot):
    switch = True if callback_data.button in {'remove', 'add'} else False
    athletes_list = sorted(user.athletes_active if switch else user.athletes_inactive, key=lambda x: x.first_name)
    current_athlete = athletes_list[callback_data.athlete_id]
    action = False if callback_data.button in {'add', 'add_inactive'} else True
    if action or (current_athlete.remain_trainings > 0 and not action):
        AthletesDB().training(current_athlete.id, callback_data.target_date, on_delete=action)
        current_athlete = Athlete(current_athlete.tg_id)
        if callback_data.button == 'remove_inactive' and current_athlete.remain_trainings:
            await callback.answer(f'{current_athlete.first_name} {current_athlete.last_name} восстановлен из архива',
                                  show_alert=True)
            await callback_main_menu(callback, user, bot)
            return
        if not current_athlete.remain_trainings:
            await callback.answer(f'{current_athlete.first_name} {current_athlete.last_name} перемещен в архив',
                                  show_alert=True)
            await callback_main_menu(callback, user, bot)
            return
        month_list = [f'2024-{str(month).zfill(2)}' for month in range(1, date.today().month + 1)]
        cur_year, cur_month = list(map(int, month_list[callback_data.current_month].split('-')))
        message_text = f'Атлет: {current_athlete.first_name} {current_athlete.last_name}\n'
        message_text += f'Тренировка за {callback_data.target_date.rsplit("-", 1)[-1]} '
        message_text += f'{rus_month[cur_month - 1].title()} {cur_year} '
        message_text += f'{"удалена" if action else "добавлена"}'
        message_media = InputMediaPhoto(media=current_athlete.photo, caption=message_text)
        await bot.edit_message_media(media=message_media, chat_id=callback.from_user.id,
                                     message_id=callback.message.message_id,
                                     reply_markup=ikb_calendar(user, current_athlete, callback_data, switch))
    else:
        await callback.answer('Нет оплаченных тренировок', show_alert=True)

# @trainings_router.callback_query(AthleteCheck.filter(F.menu == 'AtCh'))
# async def set_training_to_athlete(callback: CallbackQuery, callback_data: AthleteCheck, user: Trainer, bot: Bot):
#     athlete_id = callback_data.athlete_id
#     AthletesDB().complete_session(athlete_id)
#     TrainingsDB().add(athlete_id, 'Done')
#     await callback.answer(text=f'{callback.from_user.first_name}', show_alert=True)
#     await bot.edit_message_text(text=f'Пользователь {athlete_id} записан', chat_id=callback.from_user.id,
#                                 message_id=callback.message.message_id, reply_markup=ikb_athletes_list(user))
