from .base import DataBase


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

    def load(self, trainer_tg_id: int):
        sql = 'SELECT * FROM trainers WHERE trainer_tg_id=?'
        return super().execute(sql, (trainer_tg_id,), fetchone=True)

    def load_all(self):
        sql = 'SELECT * FROM trainers'
        return super().execute(sql, fetchall=True)

    def set_options(self, trainer_id: int, options: str):
        sql = '''UPDATE trainers SET options=? WHERE trainer_id=?'''
        super().execute(sql, (options, trainer_id,), commit=True)

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
