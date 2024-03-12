from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from datetime import date
from database.user import User
from database import AthletesDB, Athlete, TrainersDB, Trainer


#
# class TodayMiddleware(BaseMiddleware):
#     async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#                        event: TelegramObject, data: Dict[str, Any]) -> Any:
#         data['today'] = date.today().__str__()
#         return await handler(event, data)


class LoadUserInfo(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: Dict[str, Any]) -> Any:
        data['user'] = None
        if trainer := TrainersDB().load_by_tg_id(data['event_from_user'].id):
            data['user'] = Trainer(trainer[0])
        elif athlete := AthletesDB().load(data['event_from_user'].id):
            data['user'] = Athlete(athlete[1])
        return await handler(event, data)
