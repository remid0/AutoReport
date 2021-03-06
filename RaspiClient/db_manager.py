from datetime import datetime
from multiprocessing import Lock
import sqlite3

import requests

from models import User
import settings


class DBManager(object):

    def __init__(self):
        self.lock = Lock()
        with self.lock:
            self.connection = sqlite3.connect(settings.LOCAL_DB_NAME, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT * FROM sqlite_master WHERE name ='Users' and type='table'")
            if not self.cursor.fetchone():
                self.cursor.execute('''CREATE TABLE Users (
                    server_pk int PRIMARY KEY,
                    card_hash text,
                    is_authorised_to_change_mode int
                )''')
                self.cursor.execute("CREATE TABLE LastUpdate (updated_at text)")
                self.connection.commit()

    def update_local_db(self):
        with self.lock:
            now = datetime.utcnow()
            self.cursor.execute("SELECT updated_at from LastUpdate")
            last_update = self.cursor.fetchone()
            if last_update:
                results = requests.get(
                    '%susers/' % settings.SERVER_ADDRESS,
                    params={'last_update': last_update[0]}
                )
            else:
                results = requests.get('%susers/' % settings.SERVER_ADDRESS)
            if results.status_code != 200:
                raise ValueError('Fail to connect to the server')

            for user in results.json():
                self.cursor.execute("SELECT * from Users WHERE server_pk = %d" % user['id'])
                if self.cursor.fetchone():
                    self.cursor.execute(
                        '''
                        UPDATE Users
                        SET card_hash = '%s', is_authorised_to_change_mode = %d
                        WHERE server_pk = %d
                        ''' % (
                            user['card_hash'],
                            1 if user['is_authorised_to_change_mode'] else 0,
                            user['id']
                        )
                    )
                else:
                    self.cursor.execute("INSERT INTO Users VALUES (%d, '%s', %d)" % (
                        user['id'],
                        user['card_hash'],
                        1 if user['is_authorised_to_change_mode'] else 0
                    ))
            if last_update:
                self.cursor.execute(
                    "UPDATE LastUpdate SET updated_at = '%s'" %
                    now.strftime(settings.DATETIME_FORMAT)
                )
            else:
                self.cursor.execute(
                    "INSERT INTO LastUpdate VALUES ('%s')" % now.strftime(settings.DATETIME_FORMAT)
                )
            self.connection.commit()

    def get_user(self, card_uid):
        with self.lock:
            card_hash = card_uid  # TODO : calculate card_hash
            self.cursor.execute('''
                SELECT * from Users
                WHERE card_hash = '%s'
            ''' % card_hash)
            result = self.cursor.fetchone()
            if result:
                return User(
                    server_pk=result[0],
                    card_hash=result[1],
                    is_authorised_to_change_mode=result[2]
                )
