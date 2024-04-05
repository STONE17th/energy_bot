from aiogram import Router

from .trainers import trainers_router
from .trainings import trainings_router
from .main_menu import main_menu_router

inline_handlers = Router()
inline_handlers.include_routers(trainings_router, trainers_router, main_menu_router)
