from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime


db = SqliteExtDatabase('data.db')


class BaseModel(Model):
    class Meta:
        database = db


class Website(BaseModel):
    chat_id = CharField()
    url = CharField()
    created_date = DateTimeField(default=datetime.datetime.now)
    last_status_code = IntegerField(default=0)


db.connect()

if not Website.table_exists():
    db.create_tables([Website])