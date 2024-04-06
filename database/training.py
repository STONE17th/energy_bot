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

    def add(self, athlete_id: int, today_date: str = None, message: str = 'Done'):
        today = today_date or str(date.today())
        sql = 'INSERT INTO trainings (athlete_id, training_date, training_schema) VALUES (?, ?, ?)'
        super().execute(sql, (athlete_id, today, message), commit=True)

    def remove(self, athlete_id: int, target_date: str):
        sql = 'DELETE FROM trainings WHERE athlete_id=? AND training_date=?'
        super().execute(sql, (athlete_id, target_date), commit=True)

    # def athletes_data(self, athlete_id: int):
    #     sql = 'SELECT * FROM trainings WHERE athlete_id=?'
    #     if result := super().execute(sql, (athlete_id,), fetchall=True):
    #         return [Training(data) for data in result]
    #     return None

    def all_athlete_dates(self, athlete_id: int):
        sql = 'SELECT training_date FROM trainings WHERE athlete_id=?'
        return super().execute(sql, (athlete_id,), fetchall=True)
