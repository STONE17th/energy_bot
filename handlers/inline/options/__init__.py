from aiogram import Router

from .trainer import trainer_options_router

inline_options_handlers = Router()
inline_options_handlers.include_routers(trainer_options_router)
