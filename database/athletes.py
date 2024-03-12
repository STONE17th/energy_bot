from .base import DataBase
from .trainers import TrainersDB, Trainer

from datetime import date, datetime


class Athlete:
    def __new__(cls, tg_id: int):
        if athlete := AthletesDB().load(tg_id):
            instance = super().__new__(cls)
            instance.id = athlete[0]
            instance.tg_id = athlete[1]
            instance.trainer = Trainer(int(athlete[2]))
            instance.first_name = athlete[3]
            instance.last_name = athlete[4]
            instance.photo = athlete[5]
            instance.start_date = athlete[6]
            instance.total_trainings = int(athlete[7])
            instance.remain_trainings = int(athlete[8])
            return instance
        return None

    def paid(self):
        AthletesDB().paid(self.id)

        self.remain_trainings += 12
        TrainingsDB().add(self.id, f'Оплатил 12 занятий. Всего: {self.remain_trainings}')

    def complete(self):
        if self.remain_trainings > 0:
            AthletesDB().complete_session(self.id)
            self.remain_trainings -= 1
            self.total_trainings += 1
            TrainingsDB().add(self.id, f'Осталось: {self.remain_trainings}, всего провел: {self.total_trainings}')
            return True
        return False

    def for_trainer(self):
        return f'Имя: {self.first_name} {self.last_name}\nНачало занятий: {self.start_date}\nВсего занятий: {self.total_trainings}\n\nОсталось оплаченных занятий: {self.remain_trainings}'

    def __str__(self):
        return f'Атлет: {self.first_name} {self.last_name} ({self.tg_id}, {self.id})\n{self.trainer}'


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

    def load(self, athlete_tg_id: int):
        sql = 'SELECT * FROM athletes WHERE athlete_tg_id=?'
        return super().execute(sql, (athlete_tg_id,), fetchone=True)

    def load_by_id(self, athlete_id: int):
        sql = 'SELECT * FROM athletes WHERE athlete_id=?'
        return super().execute(sql, (athlete_id,), fetchone=True)

    def for_trainer_by_id(self, trainer_id: int):
        sql = 'SELECT * FROM athletes WHERE athlete_trainer_id=?'
        return super().execute(sql, (trainer_id,), fetchall=True)

    def paid(self, athlete_id: int):
        sql = 'UPDATE athletes SET remain_trainings = remain_trainings + 12 WHERE athlete_id=?'
        return super().execute(sql, (athlete_id,), commit=True)

    def complete_session(self, athlete_id: int):
        sql = 'UPDATE athletes SET total_trainings = total_trainings + 1, remain_trainings = remain_trainings - 1 WHERE athlete_id=?'
        return super().execute(sql, (athlete_id,), commit=True)


class Training:
    def __init__(self, data: tuple):
        self.id = data[0]
        self.athlete = AthletesDB().load_by_id(int(data[1]))
        self.date = data[2]
        self.message = data[3]

    def for_message(self):
        return f'{self.date}\n{self.message}\n'

    def __repr__(self):
        return f'{self.date} - {self.message}'


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

    def add(self, athlete_id: int, message: str):
        date = datetime.now().strftime('%d/%m/%y %I:%M')
        sql = 'INSERT INTO trainings (athlete_id, training_date, training_schema) VALUES (?, ?, ?)'
        super().execute(sql, (athlete_id, date, message), commit=True)

    def athletes_data(self, athlete_id: int):
        sql = 'SELECT * FROM trainings WHERE athlete_id=?'
        if result := super().execute(sql, (athlete_id,), fetchall=True):
            return [Training(data) for data in result]
        return None
