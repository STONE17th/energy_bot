from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from .states import NewAthleteState

from keyboards import ikb_edited_athlete
from keyboards.inline.callbackdata import NewAthlete

from database import AthletesDB
import settings

new_athlete_fsm_router = Router()


@new_athlete_fsm_router.callback_query(NewAthlete.filter(F.menu == 'edit'))
async def new_athlete_start(callback: CallbackQuery, state: FSMContext, callback_data: NewAthlete, bot: Bot) -> None:
    await state.set_state(NewAthleteState.first_name)
    await state.update_data(tg_id=callback_data.tg_id,
                            trainer_id=callback_data.trainer_id,
                            photo=settings.pict['new_athlete'],
                            cur_chat=callback.from_user.id,
                            cur_message=callback.message.message_id)
    data = await state.get_data()
    await bot.edit_message_media(InputMediaPhoto(media=data['photo'], caption='Введите имя атлета:'),
                                 chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id)


@new_athlete_fsm_router.message(NewAthleteState.first_name)
async def new_athlete_first_name(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(first_name=message.text)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    data = await state.get_data()
    cur_chat = data['cur_chat']
    cur_message = data['cur_message']
    await bot.edit_message_media(InputMediaPhoto(media=data['photo'], caption='Введите фамилию атлета:'),
                                 cur_chat, cur_message)
    await state.set_state(NewAthleteState.last_name)


@new_athlete_fsm_router.message(NewAthleteState.last_name)
async def new_athlete_last_name(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(last_name=message.text)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    data = await state.get_data()
    cur_chat = data['cur_chat']
    cur_message = data['cur_message']
    await bot.edit_message_media(InputMediaPhoto(media=data['photo'], caption='Сфотографируйте атлета:'),
                                 cur_chat, cur_message)
    await state.set_state(NewAthleteState.photo)


@new_athlete_fsm_router.message(NewAthleteState.photo, F.photo)
async def new_item_photo_name(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    cur_chat = data['cur_chat']
    cur_message = data['cur_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    message_text = f"Telegram ID: {data['tg_id']}\nИмя и фамилия: {data['first_name']} {data['last_name']}"
    await bot.edit_message_media(InputMediaPhoto(media=data['photo'], caption=message_text), cur_chat, cur_message,
                                 reply_markup=ikb_edited_athlete(data['tg_id'],
                                                                 data['first_name'],
                                                                 data['last_name'],
                                                                 data['trainer_id']))
    await state.set_state(NewAthleteState.finish)


@new_athlete_fsm_router.callback_query(NewAthlete.filter(F.menu == 'save'))
async def new_item_photo_name(callback: CallbackQuery, callback_data: NewAthlete, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    cur_chat = data['cur_chat']
    cur_message = data['cur_message']
    await callback.answer(f'Атлет {data["first_name"]} {data["last_name"]} добавлен в БД!')
    await bot.delete_message(chat_id=cur_chat, message_id=cur_message)
    AthletesDB().add([data['tg_id'], data['trainer_id'], data['first_name'], data['last_name'], data['photo']])
    await state.clear()


@new_athlete_fsm_router.callback_query(NewAthlete.filter(F.menu == 'reject'))
async def new_item_photo_name(callback: CallbackQuery, callback_data: NewAthlete, bot: Bot) -> None:
    await callback.answer(f'Заявка {callback_data.first_name} {callback_data.last_name} отклонена!', show_alert=True)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
