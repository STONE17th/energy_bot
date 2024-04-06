from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto

import settings

from classes import *

from keyboards import ikb_new_athlete, ikb_main_menu_trainer
from keyboards.inline.callbackdata import MainMenuCB

main_menu_router = Router()


async def callback_main_menu(callback: CallbackQuery, user: Athlete | Trainer | None, bot: Bot):
    message_text = f'Привет, {user.first_name}! Это твой бот с меню!'
    message_media = InputMediaPhoto(media=user.photo, caption=message_text)
    await bot.edit_message_media(media=message_media, chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id,
                                 reply_markup=ikb_main_menu_trainer(user))


@main_menu_router.callback_query(MainMenuCB.filter(F.menu == 'home'))
async def com_start(callback: CallbackQuery, user: Athlete | Trainer | None, bot: Bot):
    match user:
        case Athlete():
            await callback.answer('Ты атлет', show_alert=True)

        case Trainer():
            await callback_main_menu(callback, user, bot)
        case _:
            all_trainers = TrainersDB().load_all()
            await message.reply('Тебя нет в базе, запишись')


# @main_menu_router.callback_query(TrainerNavigation.filter(F.menu == 'navi_trainer'))
# async def trainer_navigation(callback: CallbackQuery, callback_data: TrainerNavigation, bot: Bot):
#     trainers_list = [Trainer(item[0]) for item in TrainersDB().load_all()]
#     current_trainer = trainers_list[callback_data.trainer_id]
#     await bot.edit_message_media(InputMediaPhoto(media=current_trainer.photo, caption=str(current_trainer)),
#                                  chat_id=callback.from_user.id, message_id=callback.message.message_id,
#                                  reply_markup=ikb_main_menu(trainers_list, callback_data.trainer_id))
#
#
# @main_menu_router.callback_query(TrainerNavigation.filter(F.menu == 'select_trainer'))
# async def trainer_select(callback: CallbackQuery, callback_data: TrainerNavigation, bot: Bot):
#     await callback.answer('Ваша заявка отправлена!', show_alert=True)
#     trainer = Trainer(callback_data.trainer_id)
#     athlete = (callback.from_user.id, callback.from_user.first_name, callback.from_user.last_name,
#                trainer.id)
#     message = f'У вас новый атлет: {callback.from_user.first_name} {callback.from_user.last_name}'
#     await bot.send_photo(trainer.tg_id, photo=settings.pict['new_athlete'],
#                          caption=message, reply_markup=ikb_new_athlete(*athlete))

# @main_menu_router.callback_query(MainMenuCB.filter(F.button == 'about'))
# async def main_menu_about(callback: CallbackQuery, callback_data: MainMenuCB, bot: Bot):
#     text_message = ('Наше объединение это люди долгие годы занимающиеся юмором и проведением мероприятий, среди нас '
#                     'есть участник телевизионных проектов (давай поженимся, вести на кубань 24, человек в маске в шоу '
#                     '"моя семья" и т.д.), дипломированный звукорежиссёр, сам Рэм Спартакович и знаменитый интервьюер '
#                     'из "Блокнот Новороссийск"')
#     await bot.edit_message_media(InputMediaPhoto(media=settings.pict['about'], caption=text_message),
#                                  chat_id=callback.from_user.id, message_id=callback.message.message_id,
#                                  reply_markup=ikb_back(callback.from_user.id))
#
#
# @main_menu_router.callback_query(MainMenuCB.filter(F.button == 'poster'))
# async def main_menu_poster(callback: CallbackQuery, callback_data: MainMenuCB, bot: Bot):
#     await callback.answer('В разработке', show_alert=True)
#
#
# @main_menu_router.callback_query(ConfirmCB.filter(F.menu == 'new_admin'))
# async def request_new_admin(callback: CallbackQuery, callback_data: MainMenuCB, bot: Bot):
#     if callback_data.button == 'accept':
#         UserDB.set_admin(callback_data.user_id)
#         message_text = 'Теперь у вас есть права админа!'
#     else:
#         message_text = 'Вам отказано'
#     await bot.send_message(callback_data.user_id, message_text)
