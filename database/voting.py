from aiogram.types import Message

from database.base import DataBase

from datetime import date


class VoteMessage:
    def __init__(self, data: tuple):
        self.id = int(data[0])
        self.date = data[1]
        self.vote_body = data[2]
        self.options = [data[3], data[4], data[5], data[6]]
        self.status = bool(data[7])


class VotingDB(DataBase):
    _instance = None

    def __new__(cls):
        if not isinstance(VotingDB._instance, cls):
            VotingDB._instance = super().__new__(cls)
        return VotingDB._instance

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS voting
        (vote_id INTEGER PRIMARY KEY, vote_date VARCHAR, vote_body VARCHAR,
        variant_1 VARCHAR, variant_2 VARCHAR,variant_3 VARCHAR,variant_4 VARCHAR, status INTEGER)'''
        super().execute(sql, commit=True)

    @staticmethod
    def load_all():
        today_date = date.today().__str__()
        sql = 'SELECT * FROM voting WHERE vote_date=?'
        return DataBase.execute(sql, (today_date,), fetchall=True)

    @staticmethod
    def load(vote_id: int):
        today_date = date.today().__str__()
        sql = 'SELECT * FROM voting WHERE vote_date=? AND vote_id=?'
        return DataBase.execute(sql, (today_date, str(vote_id)), fetchone=True)

    def activate(self, vote_id: int):
        sql = '''UPDATE voting SET status=1 WHERE vote_id=?'''
        DataBase.execute(sql, (vote_id,), commit=True)
