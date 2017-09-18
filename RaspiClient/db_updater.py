from datetime import datetime
import sqlite3

import pytz
import requests

import settings

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f %Z%z'
CONNECTION = sqlite3.connect('users_db.sqlite3')
CURSOR = CONNECTION.cursor()


def ini_db():
    CURSOR.execute("SELECT * FROM sqlite_master WHERE name ='Users' and type='table'")
    if not CURSOR.fetchone():
        CURSOR.execute('''CREATE TABLE Users (
            utc_uid int,
            card_hash text,
            is_autorized_to_change_mode int
        )''')
        CURSOR.execute("CREATE TABLE LastUpdate (updated_at text)")
        CONNECTION.commit()


def insert_new_user(new_user):
    CURSOR.execute("INSERT INTO Users VALUES (%d, '%s', %d)" % (
        new_user['utc_uid'],
        new_user['card_hash'],
        1 if new_user['is_autorized_to_change_mode'] else 0
    ))


def update_user(user):
    CURSOR.execute('''UPDATE Users
        SET card_hash = '%s', is_autorized_to_change_mode = %d
        WHERE utc_uid = %d''' % (
            user['card_hash'],
            1 if user['is_autorized_to_change_mode'] else 0,
            user['utc_uid']
        )
    )


def update_db():
    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    CURSOR.execute("SELECT updated_at from LastUpdate")
    last_update = CURSOR.fetchone()
    if last_update:
        results = requests.get(
            '%susers/' % settings.SEVER_ADDRESS,
            params={'last_update': last_update[0]}
        )
    else:
        results = requests.get('%susers/' % settings.SEVER_ADDRESS)
    if results.status_code != 200:
        raise ValueError('Fail to connect to the server')

    for user in results.json():
        CURSOR.execute("SELECT * from Users WHERE utc_uid = %d" % user['utc_uid'])
        if CURSOR.fetchone():
            update_user(user)
        else:
            insert_new_user(user)
    if last_update:
        CURSOR.execute("UPDATE LastUpdate SET updated_at = '%s'" % now.strftime(DATETIME_FORMAT))
    else:
        CURSOR.execute("INSERT INTO LastUpdate VALUES ('%s')" % now.strftime(DATETIME_FORMAT))
    CONNECTION.commit()
