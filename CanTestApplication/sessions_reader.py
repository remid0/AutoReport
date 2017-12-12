import os
import pickle

from settings import (
    LOCAL_SESSIONS_FILE,
    RPI_ID,
    RPI_LOCAL_SESSIONS_FILE,
    RPI_REMOTE_SESSIONS_FILE
)


class SessionsReader(object):

    def __init__(self, test_type):
        self.test_type = test_type

    def set_test_type(self, new_type):
        self.test_type = new_type

    def get_last_session(self):
        if self.test_type == "local":
            sessions = self.load_sessions_file(LOCAL_SESSIONS_FILE)
        else:
            try:
                os.remove(RPI_LOCAL_SESSIONS_FILE)
            except FileNotFoundError:
                pass
            os.system("scp -B %s:%s %s" % (RPI_ID, RPI_REMOTE_SESSIONS_FILE, RPI_LOCAL_SESSIONS_FILE))
            sessions = self.load_sessions_file(RPI_LOCAL_SESSIONS_FILE)
        return sessions[-1]

    def load_sessions_file(self, file_path):
        sessions = []
        with open(file_path, 'rb') as sessions_save_file:
            while True:
                try:
                    sessions.append(pickle.load(sessions_save_file))
                except EOFError:
                    break
        return sessions
