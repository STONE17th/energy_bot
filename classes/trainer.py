from database import AthletesDB, TrainersDB
from .athlete import Athlete


# from .training import Training


class Trainer:
    def __new__(cls, trainer_tg_id: int):
        if trainer := TrainersDB().load(trainer_tg_id):
            instance = super().__new__(cls)
            instance.id = trainer[0]
            instance.tg_id = int(trainer[1])
            instance.first_name = trainer[2]
            instance.last_name = trainer[3]
            instance.photo = trainer[4]
            instance.description = trainer[5]
            # instance.options = TrainerOption(trainer[6])
            return instance
        return None

    @property
    def athletes_active(self) -> list[Athlete]:
        return [Athlete(athlete[1]) for athlete in AthletesDB().my_athletes(self.id, True)]

    @property
    def athletes_inactive(self) -> list[Athlete]:
        return [Athlete(athlete[1]) for athlete in AthletesDB().my_athletes(self.id)]

    @property
    def options(self):
        return TrainerOption(TrainersDB().load(self.tg_id)[-1])

    def set_options(self, options: str):
        TrainersDB().set_options(self.id, options)

    def __str__(self):
        return f'Тренер: {self.first_name} {self.last_name} (ID:{self.id}, TG:{self.tg_id})'


class TrainerOption:
    def __init__(self, options: str):
        options_list = options.split()
        self.athletes_show = options_list[0]
        self.schedule_time = options_list[1]
        self.option_3 = options_list[2]
