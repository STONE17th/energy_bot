from aiogram import Router

from .commands import command_router
from .inline import inline_handlers

handlers_routers = Router()

handlers_routers.include_routers(command_router, inline_handlers)
