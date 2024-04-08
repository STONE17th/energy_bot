from aiogram import Bot
from aiogram.types import Message, InputMediaPhoto

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from classes import *
from database import *
from keyboards import ikb_athletes_list

from datetime import date

bot_scheduler = AsyncIOScheduler()


async def notify_trainer(bot: Bot, trainer: Trainer):
    athletes_list = TrainingsDB().not_training_today(trainer.id)
    message_text = f'Привет, {trainer.first_name}!\nПришло время отметить тех, кто был сегодня на тренировке:'
    if athletes_list:
        await bot.send_photo(chat_id=trainer.tg_id, photo=trainer.photo,
                             caption=message_text,
                             reply_markup=ikb_athletes_list(trainer))


async def add_notification(bot: Bot, trainer: Trainer):
    hours, minutes = list(map(int, [trainer.options.schedule_time[:2], trainer.options.schedule_time[2:]]))
    bot_scheduler.add_job(notify_trainer, 'cron', hour=hours, minute=minutes,
                          id=f'{trainer.tg_id}', args=[bot, trainer])


async def modify_notification(trainer: Trainer):
    hours, minutes = list(map(int, [trainer.options.schedule_time[:2], trainer.options.schedule_time[2:]]))
    print(hours, minutes)
    bot_scheduler.reschedule_job(f'{trainer.tg_id}', trigger='cron', hour=hours, minute=minutes)


async def start_scheduler(bot: Bot):
    for trainer in [Trainer(user[1]) for user in TrainersDB().load_all()]:
        await add_notification(bot, trainer)
    bot_scheduler.start()
#
#
# async def notification_trainer():
#     print('Дневник сработал')
