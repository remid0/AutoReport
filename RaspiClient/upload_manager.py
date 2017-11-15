from datetime import datetime
import json
from multiprocessing import Process
import os
import pickle
import time

import requests

from models import GpsPoint, Session
from settings import DATETIME_FORMAT, SESSION_SAVE_FILE, TIME_BETWEEN_UPLOAD


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return datetime.strftime(obj, DATETIME_FORMAT)
        if isinstance(obj, Session) or isinstance(obj, GpsPoint):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Uploader(Process):

    def __init__(self, session_manager, db_manager):
        self.session_manager = session_manager
        self.db_manager = db_manager
        super(Uploader, self).__init__()

    def run(self):
        while True:
            self.db_manager.update_local_db()
            sessions = []
            self.session_manager.acquire_file()
            with open(SESSION_SAVE_FILE, 'rb') as sessions_save_file:
                while True:
                    try:
                        sessions.append(pickle.load(sessions_save_file))
                    except EOFError:
                        break
            if sessions:
                try:
                    result = requests.post(
                        'http://localhost:8000/sessions/create/',
                        json=json.dumps(sessions, cls=MyEncoder)
                    )
                except requests.exceptions.RequestException:
                    continue
                if result.status_code == 201:  # Upload success
                    os.system('rm -f %s' % SESSION_SAVE_FILE)
            self.session_manager.release_file()
            time.sleep(TIME_BETWEEN_UPLOAD)


class UploadManager(object):

    def __init__(self, session_manager, db_manager):
        self.sub_process = Uploader(session_manager, db_manager)
        self.sub_process.start()

    def __del__(self):
        self.sub_process.terminate()
