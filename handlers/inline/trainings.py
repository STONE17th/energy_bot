from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto

from keyboards.inline.callbackdata import VotingNavigationCB
from database import AthletesDB, TrainingsDB, Trainer
from database.voting import VotingDB, VoteMessage

from keyboards.inline.callbackdata import AthleteCheck
from keyboards import ikb_athletes_list
# from keyboards.inline.voting import ikb_options

from datetime import date

trainings_router = Router()


@trainings_router.callback_query(AthleteCheck.filter(F.menu == 'AtCh'))
async def set_training_to_athlete(callback: CallbackQuery, callback_data: AthleteCheck, user: Trainer, bot: Bot):
    athlete_id = callback_data.athlete_id
    AthletesDB().complete_session(athlete_id)
    TrainingsDB().add(athlete_id, 'Done')
    await callback.answer(text=f'{callback.from_user.first_name}', show_alert=True)
    await bot.edit_message_text(text=f'Пользователь {athlete_id} записан', chat_id=callback.from_user.id,
                                message_id=callback.message.message_id, reply_markup=ikb_athletes_list(user))
