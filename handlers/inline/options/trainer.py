from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto

import settings
from classes import *

from keyboards import ikb_options_trainer
from keyboards.inline.callbackdata import TrainerOptions

trainer_options_router = Router()


@trainer_options_router.callback_query(TrainerOptions.filter(F.button.in_({'options', 'save_time', 'save_show'})))
async def trainer_options_handler(callback: CallbackQuery, user: Trainer, bot: Bot, callback_data: TrainerOptions):
    callback_data.current_show = change_show(callback_data.current_show, callback_data.new_show)
    callback_data.current_time = change_time(callback_data.current_time, callback_data.new_time)
    show_time = f'{callback_data.current_time[:2]}:{callback_data.current_time[2:]}'
    if callback_data.button == 'save_show':
        user.set_options(f'{callback_data.current_show} {user.options.schedule_time} 0')
        await callback.answer(f'Количество атлетов в группе изменено на {callback_data.current_show}',
                              show_alert=True)
    elif callback_data.button == 'save_time':
        user.set_options(f'{user.options.athletes_show} {callback_data.current_time} 0')
        await callback.answer(f'Время ежедневного оповещения изменено на {show_time}',
                              show_alert=True)
    message_text = f'{user.first_name}! Ваши настройки:\n'
    message_text += f'Показывать атлетов по {callback_data.current_show} человек\n'
    message_text += f'Время ежедневного оповещения: {show_time}'
    message_text += callback_data.refresh
    message = InputMediaPhoto(media=settings.pict['new_athlete'], caption=message_text)
    await bot.edit_message_media(media=message, chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id,
                                 reply_markup=ikb_options_trainer(callback_data))


def change_show(current_value: int, new_value: int):
    return (current_value + new_value) % 6


def change_time(current_value: str, new_value: int):
    if not new_value:
        return current_value
    hours, minutes = list(map(int, [current_value[:2], current_value[2:]]))
    if minutes == 30:
        if new_value > 0:
            return f'{str((hours + 1) % 24).zfill(2)}00'
        return f'{str(hours).zfill(2)}00'
    else:
        if new_value > 0:
            return f'{str(hours).zfill(2)}30'
        return f'{str((hours - 1) % 24).zfill(2)}30'
