import pickle

from settings import SESSION_SAVE_FILE

sessions = []
with open(SESSION_SAVE_FILE, 'rb') as sessions_save_file:
    while True:
        try:
            sessions.append(pickle.load(sessions_save_file))
        except EOFError:
            break
