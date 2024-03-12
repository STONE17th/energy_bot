from aiogram.filters.callback_data import CallbackData


class MainMenuCB(CallbackData, prefix='MM'):
    menu: str


class VotingNavigationCB(CallbackData, prefix='voting_navigation'):
    menu: str
    current_id: int
    user_id: int
    vote_id: int
    option_id: int
    refresh: str = ' '


class ConfirmCB(CallbackData, prefix='confirm'):
    menu: str
    button: str
    user_id: int


class TrainerNavigation(CallbackData, prefix='select_trainer'):
    menu: str
    trainer_id: int


class NewAthlete(CallbackData, prefix='na'):
    menu: str
    tg_id: int
    first_name: str
    last_name: str
    photo: str
    trainer_id: int


class TrainerMainMenu(CallbackData, prefix='TMM'):
    menu: str
    current_id: int
