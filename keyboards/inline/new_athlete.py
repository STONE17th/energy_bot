from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
#
from .callbackdata import NewAthlete
from database.user import User, UserDB


def ikb_new_athlete(tg_id: int, first_name: str, last_name: str, trainer_id: int, athlete_photo: str = '0'):
    keyboard = InlineKeyboardBuilder()
    add_rename(keyboard, tg_id, first_name, last_name, trainer_id, athlete_photo)
    add_reject(keyboard, tg_id, first_name, last_name, trainer_id)
    return keyboard.as_markup()


def ikb_edited_athlete(tg_id: int, first_name: str, last_name: str, trainer_id: int, athlete_photo: str = '0'):
    keyboard = InlineKeyboardBuilder()
    add_rename(keyboard, tg_id, first_name, last_name, trainer_id)
    add_save(keyboard, tg_id, first_name, last_name, trainer_id)
    return keyboard.as_markup()


def add_rename(current_keyboard: InlineKeyboardBuilder, tg_id: int, first_name: str, last_name: str, trainer_id: int,
               athlete_photo: str = '0'):
    current_keyboard.button(text='Переименовать', callback_data=NewAthlete(menu='edit',
                                                                           tg_id=tg_id,
                                                                           first_name=first_name,
                                                                           last_name=last_name,
                                                                           photo=athlete_photo,
                                                                           trainer_id=trainer_id))


def add_reject(current_keyboard: InlineKeyboardBuilder, tg_id: int, first_name: str, last_name: str, trainer_id: int,
               athlete_photo: str = '0'):
    current_keyboard.button(text='Отклонить', callback_data=NewAthlete(menu='reject',
                                                                      tg_id=tg_id,
                                                                      first_name=first_name,
                                                                      last_name=last_name,
                                                                      photo=athlete_photo,
                                                                      trainer_id=trainer_id))


def add_save(current_keyboard: InlineKeyboardBuilder, tg_id: int, first_name: str, last_name: str, trainer_id: int,
             athlete_photo: str = '0'):
    current_keyboard.button(text='Записать', callback_data=NewAthlete(menu='save',
                                                                      tg_id=tg_id,
                                                                      first_name=first_name,
                                                                      last_name=last_name,
                                                                      photo=athlete_photo,
                                                                      trainer_id=trainer_id))

# def ikb_options(user: User, vote_id: int, options_list: list[str], current_id: int, len_list: int, vote_status: int,
#                 is_admin: bool, refresh: str = ' '):
#     keyboard = InlineKeyboardBuilder()
#     new_refresh = ' ' if refresh == '.' else '.'
#     if not is_admin:
#         for option_id, option in enumerate(options_list, 1):
#             button_option(keyboard, option, user.user_tg_id, vote_id, option_id, current_id)
#     else:
#         button_admin(keyboard, user_id=user.user_tg_id, vote_id=vote_id, option=current_id, current_id=current_id,
#                      len_list=len_list, vote_status=vote_status, refresh=new_refresh)
#     button_navigation(keyboard, user_id=user.user_tg_id, vote_id=vote_id, option=current_id, current_id=current_id,
#                       len_list=len_list)
#
#     if options_list:
#         keyboard.adjust(1, 1, 1, 1, 3)
#     else:
#         keyboard.adjust(3)
#     if is_admin:
#         keyboard.adjust(1, 3)
#     return keyboard.as_markup()
#
#
# def button_option(keyboard: InlineKeyboardBuilder, text: str, user_id: int, vote_id: int, option: int,
#                   current_id: int):
#     keyboard.button(text=text,
#                     callback_data=VotingNavigationCB(menu='voting', user_id=user_id, vote_id=vote_id,
#                                                      option_id=option, current_id=current_id))
#
#
# def button_admin(keyboard: InlineKeyboardBuilder, user_id: int, vote_id: int, option: int,
#                  current_id: int, len_list: int, vote_status: int, refresh: str):
#     if not vote_status:
#         keyboard.button(text='Запуск',
#                         callback_data=VotingNavigationCB(menu='activate_vote', current_id=current_id,
#                                                          user_id=user_id, vote_id=vote_id, option_id=len_list,
#                                                          refresh=refresh))
#     else:
#         keyboard.button(text='Статистика',
#                         callback_data=VotingNavigationCB(menu='check_vote', current_id=current_id,
#                                                          user_id=user_id, vote_id=vote_id, option_id=len_list,
#                                                          refresh=refresh))
#
#
# def button_navigation(keyboard: InlineKeyboardBuilder, user_id: int, vote_id: int, option: int,
#                       current_id: int, len_list: int):
#     keyboard.button(text='<<<', callback_data=VotingNavigationCB(menu='search', current_id=(current_id - 1) % len_list,
#                                                                  user_id=user_id, vote_id=vote_id, option_id=option))
#     keyboard.button(text='МЕНЮ', callback_data=MainMenuCB(button='back', user_id=user_id, admin=0))
#     keyboard.button(text='>>>', callback_data=VotingNavigationCB(menu='search', current_id=(current_id + 1) % len_list,
#                                                                  user_id=user_id, vote_id=vote_id, option_id=option))
