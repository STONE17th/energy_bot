from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from .states import UserState

# from keyboards import ikb_confirm, ikb_select_type
# from keyboards.inline.callbackdata import UserCB, ConfirmCB
from settings import pict

# from database import User

user_registration_fsm_router = Router()


@user_registration_fsm_router.callback_query(UserCB.filter(F.button == 'start'))
async def new_user_name(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await state.set_state(UserState.name)
    await state.update_data(cur_chat=callback.message.chat.id,
                            cur_message=callback.message.message_id)
    photo = InputMediaPhoto(media=pict.get('reg'), caption='Введите ваше имя: ')
    await bot.edit_message_media(photo, callback.message.chat.id, callback.message.message_id)


@user_registration_fsm_router.message(UserState.name)
async def new_user_phone(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(name=message.text)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    data = await state.get_data()
    cur_chat = data['cur_chat']
    cur_message = data['cur_message']
    photo = InputMediaPhoto(media=pict.get('reg'), caption='Введите ваш номер телефона: ')
    await bot.edit_message_media(photo, cur_chat, cur_message)
    await state.set_state(UserState.phone)


@user_registration_fsm_router.message(UserState.phone)
async def new_user_address(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(phone=message.text)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    data = await state.get_data()
    cur_chat = data['cur_chat']
    cur_message = data['cur_message']
    photo = InputMediaPhoto(media=pict.get('reg'), caption='Введите ваш адрес (используется при доставке): ')
    await bot.edit_message_media(photo, cur_chat, cur_message)
    await state.set_state(UserState.address)


@user_registration_fsm_router.message(UserState.address)
async def new_user_address(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(address=message.text)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    data = await state.get_data()
    cur_chat = data['cur_chat']
    cur_message = data['cur_message']
    caption = f'{data["name"]}\n{data["phone"]}\n{data["address"]}\n\nДанные введены верно?'
    photo = InputMediaPhoto(media=pict.get('reg'), caption=caption)
    await state.set_state(UserState.confirm)
    await bot.edit_message_media(photo, cur_chat, cur_message, reply_markup=ikb_confirm('new_user'))


@user_registration_fsm_router.callback_query(UserState.confirm, ConfirmCB.filter(F.menu == 'new_user'))
async def new_user_confirm(callback: CallbackQuery, callback_data: ConfirmCB, state: FSMContext, bot: Bot) -> None:
    if callback_data.button == 'yes':
        data = await state.get_data()
        cur_chat = data['cur_chat']
        cur_message = data['cur_message']
        user_data = callback.from_user.id, data['name'], data['phone'], data['address'], 0, 1
        User.create(user_data)
        photo = InputMediaPhoto(media=pict.get('main'), caption='Вы успешно зарегистрированы в системе!')
        await bot.edit_message_media(photo, cur_chat, cur_message, reply_markup=ikb_select_type(user_data[0], 'main'))
        await state.clear()
    else:
        await state.set_state(UserState.name)
        await new_user_name(callback, state, bot)
