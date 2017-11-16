from datetime import datetime
import json
from multiprocessing import Process
import os
import pickle
import re
import time

import requests

from models import GpsPoint, Session
from settings import (
    DATETIME_FORMAT,
    SEVER_IP,
    SERVER_MAX_PING,
    SESSION_SAVE_FILE,
    TIME_BETWEEN_UPLOAD
)


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
            if self.is_network_connected():
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

    @classmethod
    def is_network_connected(cls):
        match = re.search(
            r'time=(?P<travel_time>\d+\.\d+) ms(?:\n|.)+(?P<received_packet>\d+) received',
            os.popen('ping -c 1 %s' % SEVER_IP).read()
        )
        return float(match.group('travel_time')) < SERVER_MAX_PING and  int(match.group('received_packet')) > 0



class UploadManager(object):

    def __init__(self, session_manager, db_manager):
        self.sub_process = Uploader(session_manager, db_manager)
        self.sub_process.start()

    def __del__(self):
        self.sub_process.terminate()
