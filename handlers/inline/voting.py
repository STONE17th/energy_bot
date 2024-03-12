from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto

from keyboards.inline.callbackdata import VotingNavigationCB
from database.user import UserDB, User
from database.voting import VotingDB, VoteMessage

# from keyboards.inline.voting import ikb_options

from datetime import date

import settings

voting_router = Router()


# @voting_router.callback_query(VotingNavigationCB.filter(F.menu == 'voting'))
# async def voting(callback: CallbackQuery, callback_data: VotingNavigationCB, bot: Bot, is_admin: bool):
#     voting_db = VotingDB()
#     current_user = User(callback_data.user_id)
#     current_user.vote(callback_data.vote_id, callback_data.option_id)
#     text_message = 'Ваш голос принят!'
#     data_list = voting_db.load_all()
#     vote_list = []
#     if data_list:
#         for item in data_list:
#             vote_list.append(VoteMessage(item))
#     current_vote = vote_list[callback_data.current_id]
#     await bot.edit_message_media(
#         media=InputMediaPhoto(media=settings.pict['vote'], caption=text_message),
#         chat_id=callback.from_user.id, message_id=callback.message.message_id,
#         reply_markup=ikb_options(user=current_user, vote_id=current_vote.id, options_list=[],
#                                  current_id=callback_data.current_id, len_list=len(vote_list), is_admin=is_admin,
#                                  vote_status=current_vote.status))
#
#
# @voting_router.callback_query(VotingNavigationCB.filter(F.menu == 'activate_vote'))
# async def activate_vote(callback: CallbackQuery, callback_data: VotingNavigationCB, bot: Bot, is_admin: bool):
#     voting_db = VotingDB()
#     current_user = User(callback_data.user_id)
#     current_vote = VoteMessage(voting_db.load(callback_data.vote_id))
#     voting_db.activate(callback_data.vote_id)
#     text_message = 'Опрос активирован!'
#     await bot.edit_message_media(
#         media=InputMediaPhoto(media=settings.pict['vote'], caption=text_message),
#         chat_id=callback.from_user.id, message_id=callback.message.message_id,
#         reply_markup=ikb_options(user=current_user, vote_id=callback_data.vote_id, options_list=[],
#                                  current_id=callback_data.current_id, len_list=callback_data.option_id,
#                                  is_admin=is_admin,
#                                  vote_status=1))
#
#
# @voting_router.callback_query(VotingNavigationCB.filter(F.menu == 'search'))
# async def voting_navigation(callback: CallbackQuery, callback_data: VotingNavigationCB, bot: Bot, is_admin: bool):
#     voting_db = VotingDB()
#     user = User(callback.from_user.id)
#     data_list = voting_db.load_all()
#     message_text = 'Голосование пока не активно'
#     vote_list = []
#     if data_list:
#         vote_list = [VoteMessage(item) for item in data_list]
#         current_vote = vote_list[callback_data.current_id]
#         message_text = f'[{callback_data.current_id + 1}/{len(vote_list)}]\n'
#         if user.check_vote(current_vote.id):
#             if vote_list[callback_data.current_id].status:
#                 message_text += current_vote.vote_body
#                 options_list = current_vote.options
#             else:
#                 if is_admin:
#                     message_text += vote_list[callback_data.current_id].vote_body
#                 else:
#                     message_text += 'Этот вопрос еще не готов\nЖдите...'
#                 options_list = []
#         else:
#             user_option = user.vote_list[vote_list[callback_data.current_id].id]
#             message_text += 'Ваш голос уже учтен, вы выбрали:\n' + vote_list[
#                 callback_data.current_id].vote_body + ": " + vote_list[callback_data.current_id].options[
#                                 user_option - 1]
#             options_list = []
#     await bot.edit_message_media(
#         media=InputMediaPhoto(media=settings.pict['vote'], caption=message_text),
#         chat_id=callback.from_user.id, message_id=callback.message.message_id,
#         reply_markup=ikb_options(user, current_vote.id, options_list,
#                                  callback_data.current_id, len(vote_list), vote_status=current_vote.status,
#                                  is_admin=is_admin))
#
#
# @voting_router.callback_query(VotingNavigationCB.filter(F.menu == 'check_vote'))
# async def voting_navigation(callback: CallbackQuery, callback_data: VotingNavigationCB, bot: Bot, is_admin: bool):
#     current_vote_id = int(callback_data.vote_id)
#     user = User(callback.from_user.id)
#     data_vote = VotingDB().load(current_vote_id)
#     result_message = 'Голосование не активно'
#     if vote := VoteMessage(data_vote) if data_vote else None:
#         users_list = UserDB().all_voting(current_vote_id)
#         result = {'total': 0, 1: 0, 2: 0, 3: 0, 4: 0}
#         for user in users_list:
#             result[user.vote_list[current_vote_id]] = result.get(user.vote_list[current_vote_id], 0) + 1
#             if current_vote_id in user.vote_list:
#                 result['total'] += 1
#         for option in result:
#             if option != 'total' and result['total']:
#                 result[option] = round(result[option] / result['total'] * 100, 2)
#             else:
#                 result[option] = 1
#         result_message = f'Проголосовало {result["total"]} человек:\n'
#         max_len = len(max(vote.options, key=len))
#         for option in sorted(result, key=lambda x: result[x], reverse=True):
#             if option != 'total':
#                 result_message += f'{vote.options[option - 1]:<{max_len}}' + ': ' + str(result[option]) + '%\n'
#     if callback_data.refresh == '.':
#         result_message += '!!!'
#     else:
#         result_message += '...'
#     await bot.edit_message_media(
#         media=InputMediaPhoto(media=settings.pict['vote'], caption=result_message),
#         chat_id=callback.from_user.id, message_id=callback.message.message_id,
#         reply_markup=ikb_options(user, current_vote_id, vote.options,
#                                  callback_data.current_id, callback_data.option_id, vote_status=vote.status,
#                                  is_admin=is_admin, refresh=callback_data.refresh))
