from aiogram import Router

# from .register_user import user_registration_fsm_router
from .new_athlete import new_athlete_fsm_router

fsm_routers = Router()

fsm_routers.include_routers(new_athlete_fsm_router)