import os
import asyncio

from aiogram import Bot, Dispatcher
from settings import *

import database
from database.voting import VotingDB
from handlers import handlers_routers
from fsm import fsm_routers
from middleware import LoadUserInfo

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

dp.update.outer_middleware(LoadUserInfo())
dp.include_routers(fsm_routers, handlers_routers)


async def start_bot():
    database.TrainersDB().create_table()
    database.AthletesDB().create_table()
    database.TrainingsDB().create_table()
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_bot())
