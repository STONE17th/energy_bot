from .base import DataBase
from datetime import date


class TrainingsDB(DataBase):
    _instance = None

    def __new__(cls):
        if not isinstance(TrainingsDB._instance, cls):
            TrainingsDB._instance = super().__new__(cls)
        return TrainingsDB._instance

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS trainings
        (
        training_id INTEGER PRIMARY KEY AUTOINCREMENT,
        athlete_id INTEGER,
        training_date VARCHAR,
        training_schema VARCHAR,
        FOREIGN KEY (athlete_id) REFERENCES athletes (athlete_id)
        )'''
        super().execute(sql, commit=True)

    def add(self, athlete_id: int, today_date: str = None, message: str = 'Training'):
        today = today_date or str(date.today())
        sql = 'INSERT INTO trainings (athlete_id, training_date, training_schema) VALUES (?, ?, ?)'
        super().execute(sql, (athlete_id, today, message), commit=True)

    def remove(self, athlete_id: int, target_date: str):
        sql = 'DELETE FROM trainings WHERE athlete_id=? AND training_date=?'
        super().execute(sql, (athlete_id, target_date), commit=True)

    def load(self, athlete_id: int):
        sql = 'SELECT training_date, training_schema FROM trainings WHERE athlete_id=?'
        return super().execute(sql, (athlete_id,), fetchall=True)

    def not_training_today(self, trainer_id: int):
        from_athletes = 'SELECT athlete_id FROM athletes WHERE athlete_trainer_id=? AND remain_trainings>?'
        from_trainings = 'SELECT athlete_id FROM trainings WHERE training_date=? AND training_schema=?'
        sql = f'{from_athletes} EXCEPT {from_trainings}'
        return super().execute(sql, (trainer_id, 0, str(date.today()), 'Training'), fetchall=True)
