from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto

import settings

from keyboards import ikb_athletes_navigation, ikb_athletes_profile_navigation, ikb_athletes_list
from keyboards.inline.callbackdata import TrainerMainMenu, TrainerMenu, AthletesMenuNavigation, AthleteCheck
from classes import *

from datetime import date

trainers_router = Router()


@trainers_router.callback_query(AthletesMenuNavigation.filter(F.button.in_({'navigate_athlete',
                                                                            'navigate_athlete_inactive'})))
async def navigate_athlete(callback: CallbackQuery, callback_data: AthletesMenuNavigation, user: Trainer, bot: Bot):
    switch = True if callback_data.button == 'navigate_athlete' else False
    len_list = len(user.athletes_active if switch else user.athletes_inactive)
    shift = int(user.options.athletes_show)
    current_id = callback_data.list_id
    message_text = f'[{current_id + 1}/{len_list // shift + bool(len_list % shift)}]'
    message_media = InputMediaPhoto(media=settings.pict['new_athlete'], caption=message_text)
    await bot.edit_message_media(media=message_media, chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id,
                                 reply_markup=ikb_athletes_navigation(user, callback_data, switch))


@trainers_router.callback_query(
    AthletesMenuNavigation.filter(F.button.in_({'select_athlete', 'select_athlete_inactive'})))
async def select_athlete(callback: CallbackQuery, callback_data: AthletesMenuNavigation, user: Trainer, bot: Bot):
    switch = True if callback_data.button == 'select_athlete' else False
    athletes_list = sorted(user.athletes_active if switch else user.athletes_inactive, key=lambda x: x.first_name)
    if athletes_list:
        current_athlete = athletes_list[callback_data.athlete_id]
        message_text = f'[{callback_data.athlete_id + 1}/{len(athletes_list)}]\n'
        message_text += f'{current_athlete.first_name} {current_athlete.last_name}\n'
        message_text += f'Дата начала тренировок: {current_athlete.start_date}\n'
        message_text += f'Тренировок завершено: {current_athlete.total_trainings}\n'
        message_text += f'Тренировок осталось: {current_athlete.remain_trainings}'
        message_photo = current_athlete.photo
    else:
        message_text = 'Пока этот список пуст'
        message_photo = settings.pict['new_athlete']
    message_media = InputMediaPhoto(media=message_photo, caption=message_text)
    await bot.edit_message_media(media=message_media, chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id,
                                 reply_markup=ikb_athletes_profile_navigation(user, callback_data, switch))


@trainers_router.callback_query(AthleteCheck.filter(F.button == 'add_today_training'))
async def athletes_training_today(callback: CallbackQuery, callback_data: AthleteCheck, user: Trainer, bot: Bot):
    athlete = Athlete(callback_data.athlete_id, tg_id=False)
    athlete.training(str(date.today()))
    message_media = InputMediaPhoto(media=settings.pict['new_athlete'],
                                    caption=f'{athlete.first_name} {athlete.last_name} записан на сегодня!')
    await bot.edit_message_media(media=message_media,
                                 chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id,
                                 reply_markup=ikb_athletes_list(user))


@trainers_router.callback_query(TrainerMenu.filter(F.menu == 'AN'))
async def athletes_navigation(callback: CallbackQuery, callback_data: TrainerMenu, user: Trainer, bot: Bot):
    athletes_list = sorted(user.athletes, key=lambda x: x.first_name)
    # athletes_list = sorted([Athlete(user[1]) for user in AthletesDB().for_trainer_by_id(user.id)],
    #                        key=lambda x: x.first_name)
    print(athletes_list, 'Новый список')
    today = str(date.today())
    today_not_training = AthletesDB().today_not_training(user.id, today)
    if user.options.athletes_show and not callback_data.items:
        list_range = int(user.options.athletes_show)
        list_of_athletes_list = [athletes_list[list_range * l_range:list_range * l_range + list_range]
                                 for l_range in range(len(athletes_list) // list_range + 1)]
        counter = f'[{callback_data.current_list_id + 1}/{len(list_of_athletes_list)}]\n'
        photo_and_caption = InputMediaPhoto(media=settings.pict['new_athlete'], caption=counter)
        await bot.edit_message_media(chat_id=callback.from_user.id,
                                     message_id=callback.message.message_id,
                                     media=photo_and_caption,
                                     reply_markup=ikb_athletes_navigation_list(int(callback_data.current_list_id),
                                                                               list_of_athletes_list))
    else:
        cur_athlete = athletes_list[callback_data.current_id]
        trained = cur_athlete in today_not_training
        print(trained)
        counter = f'[{callback_data.current_id + 1}/{len(athletes_list)}]\n'
        if callback_data.profile:
            message_text = cur_athlete.for_trainer()
        else:
            cur_athlete = athletes_list[callback_data.current_id]
            request = TrainingsDB().athletes_data(cur_athlete.id)
            request = [item.for_message() for item in request] if request else ['Записей нет']
            message_text = ''.join([f'{cur_athlete.first_name} {cur_athlete.last_name}:\n'] + request[-12:])
        photo_and_caption = InputMediaPhoto(media=cur_athlete.photo, caption=counter + message_text)
        await bot.edit_message_media(chat_id=callback.from_user.id,
                                     message_id=callback.message.message_id,
                                     media=photo_and_caption,
                                     reply_markup=ikb_athletes_navigation_items(int(callback_data.current_id),
                                                                                athletes_list, callback_data.profile,
                                                                                trained))


@trainers_router.callback_query(TrainerMainMenu.filter(F.menu == 'AN_pay'))
async def athletes_paid(callback: CallbackQuery, callback_data: TrainerMainMenu, user: Trainer, bot: Bot):
    athletes_list = [Athlete(user[1]) for user in AthletesDB().for_trainer_by_id(user.id)]
    cur_athlete = athletes_list[callback_data.current_id]
    cur_athlete.paid()
    counter = f'[{callback_data.current_id + 1}/{len(athletes_list)}]\n'
    photo_and_caption = InputMediaPhoto(media=cur_athlete.photo, caption=counter + cur_athlete.for_trainer())
    await callback.answer(f'{cur_athlete.first_name} оплатил месяц и у него {cur_athlete.remain_trainings} занятий',
                          show_alert=True)
    await bot.edit_message_media(chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id,
                                 media=photo_and_caption,
                                 reply_markup=ikb_athletes_navigation(user,
                                                                      len(athletes_list),
                                                                      int(callback_data.current_id)))


@trainers_router.callback_query(TrainerMenu.filter(F.menu == 'AN_finish'))
async def athletes_complete(callback: CallbackQuery, callback_data: TrainerMainMenu, user: Trainer, bot: Bot):
    athletes_list = [Athlete(user[1]) for user in AthletesDB().for_trainer_by_id(user.id)]
    cur_athlete = athletes_list[callback_data.current_id]
    if cur_athlete.complete():
        counter = f'[{callback_data.current_id + 1}/{len(athletes_list)}]\n'
        photo_and_caption = InputMediaPhoto(media=cur_athlete.photo, caption=counter + cur_athlete.for_trainer())
        await callback.answer(f'Занятие завершено! У {cur_athlete.first_name} осталось {cur_athlete.remain_trainings}',
                              show_alert=True)
        await bot.edit_message_media(chat_id=callback.from_user.id,
                                     message_id=callback.message.message_id,
                                     media=photo_and_caption,
                                     reply_markup=ikb_athletes_navigation(user,
                                                                          len(athletes_list),
                                                                          int(callback_data.current_id)))
    else:
        await callback.answer(f'У {cur_athlete.first_name} нет оплаченных занятий!',
                              show_alert=True)


@trainers_router.callback_query(TrainerMainMenu.filter(F.menu == 'AA'))
async def athletes_archive(callback: CallbackQuery, callback_data: TrainerMainMenu, user: Trainer, bot: Bot):
    athletes_list = [Athlete(user[1]) for user in AthletesDB().for_trainer_by_id(user.id)]
    cur_athlete = athletes_list[callback_data.current_id]
    request = TrainingsDB().athletes_data(cur_athlete.id)
    request = [item.for_message() for item in request] if request else ['Записей нет']
    athlete_archive = [f'{cur_athlete.first_name} {cur_athlete.last_name}:\n'] + request[-12:]
    photo_and_caption = InputMediaPhoto(media=cur_athlete.photo, caption='\n'.join(athlete_archive))
    await bot.edit_message_media(chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id,
                                 media=photo_and_caption,
                                 reply_markup=ikb_athletes_navigation(user,
                                                                      len(athletes_list),
                                                                      int(callback_data.current_id)))
