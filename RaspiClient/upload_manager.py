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
    SESSION_UPLOAD_FILE,
    SESSION_UPLOAD_FILE_FILTER,
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
                sessions = []
                for file_name in self.move_file_and_get_list():
                    with open(file_name, 'rb') as sessions_save_file:
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
                        if result.status_code == requests.codes.created:
                            os.system('rm -f %s' % file_name)
                time.sleep(TIME_BETWEEN_UPLOAD)

    @classmethod
    def is_network_connected(cls):
        match = re.search(
            r'time=(?P<travel_time>\d+\.\d+) ms(?:\n|.)+(?P<received_packet>\d+) received',
            os.popen('ping -c 1 %s' % SEVER_IP).read()
        )
        return float(match.group('travel_time')) < SERVER_MAX_PING and  int(match.group('received_packet')) > 0

    def move_file_and_get_list(self):
        if not os.path.isfile(SESSION_SAVE_FILE):
            return []
        file_list = [
            int(re.match(SESSION_UPLOAD_FILE_FILTER, file_name).group())
            for file_name in os.listdir()
            if re.match(SESSION_UPLOAD_FILE_FILTER, file_name)
        ]
        new_file_index = max([
            int(re.match(SESSION_UPLOAD_FILE_FILTER, file_name).group(1))
            for file_name in file_list
        ]) + 1 if file_list else 1
        self.session_manager.acquire_file()
        os.rename(SESSION_SAVE_FILE, SESSION_UPLOAD_FILE % new_file_index)
        self.session_manager.release_file()
        file_list.append(SESSION_UPLOAD_FILE % new_file_index)
        return file_list


class UploadManager(object):

    def __init__(self, session_manager, db_manager):
        self.sub_process = Uploader(session_manager, db_manager)
        self.sub_process.start()

    def __del__(self):
        self.sub_process.terminate()
