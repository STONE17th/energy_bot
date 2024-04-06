from .base import DataBase
from .training import TrainingsDB

from datetime import date


class AthletesDB(DataBase):
    _instance = None

    def __new__(cls):
        if not isinstance(AthletesDB._instance, cls):
            AthletesDB._instance = super().__new__(cls)
        return AthletesDB._instance

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS athletes
        (
        athlete_id INTEGER PRIMARY KEY AUTOINCREMENT,
        athlete_tg_id INTEGER,
        athlete_trainer_id INTEGER,
        first_name VARCHAR,
        last_name VARCHAR,
        photo VARCHAR,
        start_date VARCHAR,
        total_trainings INTEGER,
        remain_trainings INTEGER,
        FOREIGN KEY (athlete_trainer_id) REFERENCES trainers (trainer_id)
        )'''
        super().execute(sql, commit=True)

    def add(self, new_user: list):
        sql = '''INSERT INTO athletes 
               (
               athlete_tg_id,
               athlete_trainer_id,
               first_name,
               last_name,
               photo,
               start_date,
               total_trainings,
               remain_trainings
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        athlete = new_user + [date.today().strftime('%d/%m/%Y'), 0, 0]
        super().execute(sql, (*athlete,), commit=True)

    def load(self, athlete_tg_id: int, tg_id: bool = True):
        if tg_id:
            sql = 'SELECT * FROM athletes WHERE athlete_tg_id=?'
        else:
            sql = 'SELECT * FROM athletes WHERE athlete_id=?'
        return super().execute(sql, (athlete_tg_id,), fetchone=True)

    def my_athletes(self, trainer_id: int, active: bool = False) -> tuple[list]:
        if active:
            sql = 'SELECT * FROM athletes WHERE athlete_trainer_id=? AND remain_trainings > 0'
        else:
            sql = 'SELECT * FROM athletes WHERE athlete_trainer_id=? AND remain_trainings = 0'
        return super().execute(sql, (trainer_id,), fetchall=True)

    # def load_by_id(self, athlete_id: int):
    #     sql = 'SELECT * FROM athletes WHERE athlete_id=?'
    #     return super().execute(sql, (athlete_id,), fetchone=True)

    # def today_not_training(self, trainer_id: int, today: str):
    #     sql = 'SELECT * FROM athletes WHERE athlete_trainer_id=?'
    #     all_athletes = set(super().execute(sql, (trainer_id,), fetchall=True))
    #     sql = 'SELECT athlete_id FROM trainings WHERE training_date=?'
    #     today_athletes = super().execute(sql, (today,), fetchall=True)
    #     today_athletes = {athlete[0] for athlete in today_athletes} if today_athletes else set()
    #     return [Athlete(user[1]) for user in all_athletes if user[0] not in today_athletes]

    def paid(self, athlete_id: int, pay_amount: int):
        sql = f'UPDATE athletes SET remain_trainings = remain_trainings + {pay_amount} WHERE athlete_id=?'
        return super().execute(sql, (athlete_id,), commit=True)

    def training(self, athlete_id: int, target_date: str, on_delete: bool = False):
        if on_delete:
            mes = ['total_trainings = total_trainings - 1', 'remain_trainings = remain_trainings + 1']
            TrainingsDB().remove(athlete_id, target_date)
        else:
            mes = ['total_trainings = total_trainings + 1', 'remain_trainings = remain_trainings - 1']
            TrainingsDB().add(athlete_id, target_date)
        sql = f'UPDATE athletes SET {mes[0]}, {mes[1]} WHERE athlete_id=?'
        super().execute(sql, (athlete_id,), commit=True)
