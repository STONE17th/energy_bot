# from .main_menu import ikb_select_type
# from .confirm import ikb_confirm
# from .catalog import ikb_catalog_navigation
# __all__ = ['ikb_select_type', 'ikb_confirm', 'ikb_catalog_navigation']

from .main_menu import ikb_main_menu
from .new_athlete import ikb_new_athlete, ikb_edited_athlete
from .trainers import ikb_trainer_main_menu, ikb_athletes_navigation

__all__ = [
    'ikb_main_menu',
    'ikb_new_athlete',
    'ikb_edited_athlete',
    'ikb_trainer_main_menu',
    'ikb_athletes_navigation'
]
