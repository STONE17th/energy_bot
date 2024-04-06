from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from datetime import date
from database import AthletesDB, TrainersDB
from classes import Athlete, Trainer


#
# class TodayMiddleware(BaseMiddleware):
#     async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#                        event: TelegramObject, data: Dict[str, Any]) -> Any:
#         data['today'] = date.today().__str__()
#         return await handler(event, data)


class LoadDBInfo(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: Dict[str, Any]) -> Any:
        trainer = Trainer(data['event_from_user'].id)
        athlete = Athlete(data['event_from_user'].id)
        data['user'] = trainer if trainer else athlete
        return await handler(event, data)
