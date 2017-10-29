from enum import Enum


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
GPS_DEVICE = '/dev/ttyUSB0'
LOCAL_DB_NAME = 'users_db.sqlite3'
SEVER_ADDRESS = 'http://127.0.0.1:8000/'
SESSION_SAVE_FILE = 'sessions.sav'


class MODE(Enum):
    MANUAL_DRIVING = 'MAN'
    COOPERATIVE_DRIVING = 'COP'
    AUTONOMOUS_DRIVING = 'AUT'


# Load local settings
try:
    # pylint: disable=line-too-long,unused-wildcard-import,wildcard-import,wrong-import-position
    from local_settings import *
except ImportError:
    pass
