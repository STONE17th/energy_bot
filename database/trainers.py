from .base import DataBase


class TrainerOption:
    def __init__(self, options: str):
        options_list = options.split()
        self.athletes_show = options_list[0]
        self.schedule_time = options_list[1]
        self.option_3 = options_list[2]


class Trainer:
    def __new__(cls, trainer_id: int):
        if trainer := TrainersDB().load(trainer_id):
            instance = super().__new__(cls)
            instance.id = trainer[0]
            instance.tg_id = trainer[1]
            instance.first_name = trainer[2]
            instance.last_name = trainer[3]
            instance.photo = trainer[4]
            instance.description = trainer[5]
            instance.options = TrainerOption(trainer[6])
            return instance
        return None

    def __str__(self):
        return f'Тренер: {self.first_name} {self.last_name} ({self.tg_id}, {self.id})'


class TrainersDB(DataBase):
    _instance = None

    def __new__(cls):
        if not isinstance(TrainersDB._instance, cls):
            TrainersDB._instance = super().__new__(cls)
        return TrainersDB._instance

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS trainers
        (
        trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        trainer_tg_id INTEGER,
        first_name VARCHAR,
        last_name VARCHAR,
        photo_id VARCHAR,
        descriptions VARCHAR,
        options VARCHAR
        )'''
        super().execute(sql, commit=True)

    def load(self, trainer_id: int):
        sql = 'SELECT * FROM trainers WHERE trainer_id=?'
        return super().execute(sql, (trainer_id,), fetchone=True)

    def load_by_tg_id(self, trainer_id: int):
        sql = 'SELECT * FROM trainers WHERE trainer_tg_id=?'
        return super().execute(sql, (trainer_id,), fetchone=True)

    def load_all(self):
        sql = 'SELECT * FROM trainers'
        return super().execute(sql, fetchall=True)

    # def _is_exists(self, user_id):
    #     sql = 'SELECT * FROM users WHERE user_tg_id=?'
    #     return super().execute(sql, (user_id,), fetchone=True)
    #
    # def add(self, new_user: tuple):
    #     sql = 'INSERT INTO users (user_tg_id, first_name, last_name, user_name, is_admin) VALUES (?, ?, ?, ?, ?)'
    #     super().execute(sql, new_user, commit=True)
    #
    # @classmethod
    # def set_admin(cls, new_user: int):
    #     sql = '''UPDATE users SET is_admin=1 WHERE user_tg_id=?'''
    #     cls.execute(sql, (new_user,), commit=True)
    #
    # def all(self):
    #     sql = 'SELECT * FROM users'
    #     return self.execute(sql, fetchall=True)
    #
    # def all_voting(self, vote_id: int) -> list[User]:
    #     sql = 'SELECT * FROM users'
    #     users_list = self.execute(sql, fetchall=True)
    #     return [User(user[1]) for user in users_list if vote_id in set(eval(user[-1]) if user[-1] else [])]
