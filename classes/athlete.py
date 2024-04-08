from database import AthletesDB, TrainingsDB
from .calendar import Month

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
        current_year = date.today().year
        current_month = date.today().month
        result = {f'{current_year}-{str(current_month).zfill(2)}': [[], []]}
        if data_from_db := TrainingsDB().load(self.id):
            for day in data_from_db:
                cur_month = day[0].rsplit('-', 1)[0]
                cur_day = int(day[0].rsplit('-', 1)[1])
                if cur_month in result:
                    if day[1] == 'Training':
                        result[cur_month][0].append(cur_day)
                    else:
                        result[cur_month][1].append((cur_day, int(day[1].split()[1])))
                else:
                    if day[1] == 'Training':
                        result[cur_month] = [[cur_day], []]
                    else:
                        result[cur_month] = [[], [(cur_day, int(day[1].split()[1]))]]
        return {month_year: Month(month_year, *days) for month_year, days in result.items()}

    def paid(self, pay_amount: int):
        AthletesDB().paid(self.id, pay_amount)
        self.remain_trainings += pay_amount
        TrainingsDB().add(self.id, str(date.today()), f'Payment {pay_amount}')

    def training(self, training_date: str, on_delete: bool = False):
        if on_delete:
            AthletesDB().training(self.id, training_date, on_delete=True)
            self.remain_trainings += 1
            self.total_trainings -= 1
            return True
        else:
            if self.remain_trainings > 0:
                AthletesDB().training(self.id, training_date)
                self.remain_trainings -= 1
                self.total_trainings += 1
                return True
            return False

    def __str__(self):
        return f'Атлет: {self.first_name} {self.last_name} (ID:{self.id}, TG:{self.tg_id})'

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.id == other.id
        return False
