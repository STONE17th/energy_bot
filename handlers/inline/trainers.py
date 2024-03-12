from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto

import settings

from keyboards import ikb_athletes_navigation
from keyboards.inline.callbackdata import TrainerMainMenu
# from keyboards.inline.main_menu import ikb_back
from database import AthletesDB, Athlete, Trainer, TrainingsDB

#
trainers_router = Router()


@trainers_router.callback_query(TrainerMainMenu.filter(F.menu == 'AN'))
async def athletes_navigation(callback: CallbackQuery, callback_data: TrainerMainMenu, user: Trainer, bot: Bot):
    athletes_list = [Athlete(user[1]) for user in AthletesDB().for_trainer_by_id(user.id)]
    if user.options.athletes_show:
        cur_athlete = athletes_list[callback_data.current_id]
        counter = f'[{callback_data.current_id + 1}/{len(athletes_list)}]\n'
        photo_and_caption = InputMediaPhoto(media=cur_athlete.photo, caption=counter + cur_athlete.for_trainer())
        await bot.edit_message_media(chat_id=callback.from_user.id,
                                     message_id=callback.message.message_id,
                                     media=photo_and_caption,
                                     reply_markup=ikb_athletes_navigation(user,
                                                                          len(athletes_list),
                                                                          int(callback_data.current_id)))
    else:
        pass


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


@trainers_router.callback_query(TrainerMainMenu.filter(F.menu == 'AN_finish'))
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

    # text_message = ('Наше объединение это люди долгие годы занимающиеся юмором и проведением мероприятий, среди нас '
    #                 'есть участник телевизионных проектов (давай поженимся, вести на кубань 24, человек в маске в шоу '
    #                 '"моя семья" и т.д.), дипломированный звукорежиссёр, сам Рэм Спартакович и знаменитый интервьюер '
    #                 'из "Блокнот Новороссийск"')
    # await bot.edit_message_media(InputMediaPhoto(media=settings.pict['about'], caption=text_message),
    #                              chat_id=callback.from_user.id, message_id=callback.message.message_id,
    #                              reply_markup=ikb_back(callback.from_user.id))
