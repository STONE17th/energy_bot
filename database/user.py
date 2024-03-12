from aiogram.types import Message

from database.base import DataBase

import settings


# from .adapter import MessageAdapter

def data_to_tuple(data: int | tuple | Message) -> tuple:
    if isinstance(data, int):
        return (data,)
    elif isinstance(data, tuple):
        return data
    else:
        return data.from_user.id, data.from_user.first_name, data.from_user.last_name, data.from_user.username


class User(DataBase):

    def __init__(self, data: int | Message | tuple):
        self.db = UserDB()
        self.user_tg_id = data_to_tuple(data)[0]
        if not self._load():
            user_data = data_to_tuple(data) + ((True if self.user_tg_id == settings.SUPER_ADMIN_TG_ID else False), None)
            self._save(user_data)
        user_data = self._load()
        self.first_name = user_data[2]
        self.last_name = user_data[3]
        self.user_name = user_data[4]
        self.is_admin = bool(int(user_data[5]))
        self.vote_list = eval(user_data[6]) if user_data[6] else {}

    def _load(self):
        sql = 'SELECT * FROM users WHERE user_tg_id=?'
        return self.db.execute(sql, (self.user_tg_id,), fetchone=True)

    def _save(self, new_user: tuple):
        sql = 'INSERT INTO users (user_tg_id, first_name, last_name, user_name, is_admin, vote_list) VALUES (?, ?, ?, ?, ?, ?)'
        self.db.execute(sql, (*new_user,), commit=True)

    def all(self):
        sql = 'SELECT * FROM users'
        return self.db.execute(sql, fetchall=True)

    def check_vote(self, vote_id: int):
        sql = 'SELECT vote_list FROM users WHERE user_tg_id=?'
        vote_list = self.db.execute(sql, (self.user_tg_id,), fetchone=True)
        vote_list = eval(vote_list[0]) if vote_list[0] else {}
        if vote_id in vote_list:
            return False
        return True

    def vote(self, vote_id: int, variant_id: int):
        sql = 'SELECT vote_list FROM users WHERE user_tg_id=?'
        vote_list = self.db.execute(sql, (self.user_tg_id,), fetchone=True)
        vote_list = eval(vote_list[0]) if vote_list[0] else {}
        vote_list[vote_id] = variant_id
        sql = '''UPDATE users SET vote_list=? WHERE user_tg_id=?'''
        self.db.execute(sql, (str(vote_list), self.user_tg_id), commit=True)

    def __str__(self):
        return f'{self.user_tg_id} {self.first_name} {self.last_name} {self.user_name} {self.is_admin} {self.vote_list}'


class UserDB(DataBase):
    _instance = None

    def __new__(cls):
        if not isinstance(UserDB._instance, cls):
            UserDB._instance = super().__new__(cls)
        return UserDB._instance

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users
        (user_id INTEGER PRIMARY KEY, user_tg_id INTEGER, first_name VARCHAR, last_name VARCHAR,
        user_name VARCHAR, is_admin INTEGER, vote_list VARCHAR)'''
        super().execute(sql, commit=True)

    def _is_exists(self, user_id):
        sql = 'SELECT * FROM users WHERE user_tg_id=?'
        return super().execute(sql, (user_id,), fetchone=True)

    def add(self, new_user: tuple):
        sql = 'INSERT INTO users (user_tg_id, first_name, last_name, user_name, is_admin) VALUES (?, ?, ?, ?, ?)'
        super().execute(sql, new_user, commit=True)

    @classmethod
    def set_admin(cls, new_user: int):
        sql = '''UPDATE users SET is_admin=1 WHERE user_tg_id=?'''
        cls.execute(sql, (new_user,), commit=True)

    def all(self):
        sql = 'SELECT * FROM users'
        return self.execute(sql, fetchall=True)

    def all_voting(self, vote_id: int) -> list[User]:
        sql = 'SELECT * FROM users'
        users_list = self.execute(sql, fetchall=True)
        return [User(user[1]) for user in users_list if vote_id in set(eval(user[-1]) if user[-1] else [])]
