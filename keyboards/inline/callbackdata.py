from aiogram.filters.callback_data import CallbackData


class MainMenuCB(CallbackData, prefix='MM'):
    menu: str


class TrainerOptions(CallbackData, prefix='TO'):
    button: str
    current_show: int = 0
    new_show: int = 0
    current_time: str = '00 00'
    new_time: int = 0
    refresh: str = '.'


class AthletesMenuNavigation(CallbackData, prefix='AMN'):
    button: str
    list_len: int = 0
    list_id: int = 0
    athletes_count: int = 0
    athlete_id: int = 0


class TrainingCalendar(CallbackData, prefix='TC'):
    button: str
    view: str = 'Training'
    list_athlete_id: int = 0
    athlete_id: int = 0
    current_month: int = 0
    target_date: str = '0000-00-00'


class TrainerMenu(CallbackData, prefix='TM'):
    menu: str
    current_list_id: int = 0
    current_id: int = 0
    items: bool = False
    profile: bool = True


class TrainerMainMenu(CallbackData, prefix='TMM'):
    menu: str
    current_list_id: int = 0
    current_id: int = 0


class AthletePayment(CallbackData, prefix='AP'):
    button: str
    athlete_id: int = 0
    pay_amount: int = 0


class ConfirmCB(CallbackData, prefix='confirm'):
    menu: str
    button: str
    user_id: int


class NewAthlete(CallbackData, prefix='na'):
    menu: str
    tg_id: int
    first_name: str
    last_name: str
    photo: str
    trainer_id: int


class AthleteCheck(CallbackData, prefix='ac'):
    button: str
    athlete_id: int
