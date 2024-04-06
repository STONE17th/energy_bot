from database import AthletesDB, TrainingsDB
from .calendar import TrainingMonth

from datetime import date


class Athlete:
    def __new__(cls, athlete_tg_id: int, tg_id: bool = True):
        if athlete := AthletesDB().load(athlete_tg_id, tg_id):
            instance = super().__new__(cls)
            instance.id = athlete[0]
            instance.tg_id = athlete[1]
            instance.trainer_id = int(athlete[2])
            instance.first_name = athlete[3]
            instance.last_name = athlete[4]
            instance.photo = athlete[5]
            instance.start_date = athlete[6]
            instance.total_trainings = int(athlete[7])
            instance.remain_trainings = int(athlete[8])
            return instance
        return None

    @property
    def calendar(self):
        result = {f'2024-{str(month).zfill(2)}': [] for month in range(date.today().month, 0, -1)}
        all_dates = []
        if data_from_db := TrainingsDB().all_athlete_dates(self.id):
            all_dates = [t_date[0] for t_date in data_from_db]
        for cur_date in all_dates:
            m_y, day = cur_date.rsplit('-', 1)
            result[m_y].append(int(day))
        return {m_y: TrainingMonth(m_y, days) for m_y, days in result.items()}

    def paid(self, pay_amount: int):
        AthletesDB().paid(self.id, pay_amount)
        self.remain_trainings += pay_amount
        TrainingsDB().add(self.id, str(date.today()), 'Payment')

    def training(self, training_date: str, on_delete: bool = False):
        if on_delete:
            AthletesDB().target_date(self.id, training_date, on_delete=True)
            self.remain_trainings += 1
            self.total_trainings -= 1
            return True
        else:
            if self.remain_trainings > 0:
                AthletesDB().target_date(self.id, training_date)
                self.remain_trainings -= 1
                self.total_trainings += 1
                return True
            return False

    def for_trainer(self):
        return f'Имя: {self.first_name} {self.last_name}\nНачало занятий: {self.start_date}\nВсего занятий: {self.total_trainings}\n\nОсталось оплаченных занятий: {self.remain_trainings}'

    def __str__(self):
        return f'Атлет: {self.first_name} {self.last_name} (ID:{self.id}, TG:{self.tg_id})'

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.id == other.id
        return False
