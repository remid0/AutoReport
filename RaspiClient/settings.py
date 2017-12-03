from enum import Enum


CAN_BUS_TYPE = 'socketcan_native'
CAN_VEHICLE_CHANNEL = 'can0'
CAN_MABX_CHANNEL = 'can1'

LOG_FILE = 'debug.log'
LOG_FORMAT = '%(asctime)s => %(message)s'

LAST_GPS_POINT_FILE = 'gps.sav'

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
LOCAL_DB_NAME = 'users_db.sqlite3'

SEVER_IP = '127.0.0.1'
SEVER_PORT = 8000
SEVER_ADDRESS = 'http://%s:%d/' % (SEVER_IP, SEVER_PORT)
SERVER_MAX_PING = 0.500  # 500 ms
SESSION_SAVE_FILE = 'sessions.sav'
SESSION_UPLOAD_FILE = 'to_upload_%d.sav'
SESSION_UPLOAD_FILE_FILTER = r'^upload_([0-9]+)\.txt$'
TIME_BETWEEN_UPLOAD = 300  # 5 min


class MODE(Enum):
    MANUAL_DRIVING = 'MAN'
    COOPERATIVE_DRIVING = 'COP'
    AUTONOMOUS_DRIVING = 'AUT'
    UNKNOWN = 'UKN'


class STATUS_CODE(Enum):
    LOGIN = 1
    LOGOUT = 2


GPIO_AUTHORISATION_OUTPUT = 12  # Free GPIO : 12 16 18 19 20 21 23

# Load local settings
try:
    from local_settings import *
except ImportError:
    pass
