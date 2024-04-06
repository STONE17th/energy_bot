# from .main_menu import ikb_select_type
# from .confirm import ikb_confirm
# from .catalog import ikb_catalog_navigation
# __all__ = ['ikb_select_type', 'ikb_confirm', 'ikb_catalog_navigation']

from .calendar import ikb_calendar
from .options import ikb_options_trainer
from .new_athlete import ikb_new_athlete, ikb_edited_athlete
from .trainers import ikb_athletes_navigation, ikb_athletes_profile_navigation
from .trainings import ikb_athletes_list
from .main_menu import ikb_main_menu_trainer
from .payment import ikb_athlete_payment_amount

__all__ = [
    'ikb_new_athlete',
    'ikb_edited_athlete',
    'ikb_main_menu_trainer',
    'ikb_athletes_navigation',
    'ikb_athletes_profile_navigation',
    'ikb_athletes_list',
    'ikb_options_trainer',
    'ikb_calendar',
    'ikb_athlete_payment_amount'
]
