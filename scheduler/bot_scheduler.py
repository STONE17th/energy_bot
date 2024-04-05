from aiogram import Bot
from aiogram.types import Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import TrainersDB, Trainer, AthletesDB, Athlete
from keyboards import ikb_athletes_list

from datetime import date

bot_scheduler = AsyncIOScheduler()


async def notify_trainer(bot: Bot, trainer: Trainer):
    message = f'Привет, {trainer.first_name}!\nПришло время отметить тех, кто был сегодня на тренировке:'
    await bot.send_message(trainer.tg_id, text=message, reply_markup=ikb_athletes_list(trainer))


async def add_notification(bot: Bot, trainer: Trainer):
    hours, minutes = list(map(int, trainer.options.schedule_time.split(':')))
    bot_scheduler.add_job(notify_trainer, 'cron', hour=hours, minute=minutes,
                          id=f'{trainer.tg_id}', args=[bot, trainer])


async def modify_notification(trainer: Trainer):
    hours, minutes = list(map(int, trainer.options.schedule_time.split(':')))
    bot_scheduler.reschedule_job(f'{trainer.tg_id}', trigger='cron', hour=hours, minute=minutes)


async def start_scheduler(bot: Bot):
    for trainer in [Trainer(user[0]) for user in TrainersDB().load_all()]:
        await add_notification(bot, trainer)
    bot_scheduler.start()


async def notification_trainer():
    print('Дневник сработал')
