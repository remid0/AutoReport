from enum import Enum

# Files
OUTPUT_DIRECTORY = 'output'

LAST_GPS_POINT_FILE = '%s/gps.sav' % OUTPUT_DIRECTORY
LOG_FILE = '%s/debug.log' % OUTPUT_DIRECTORY
SESSION_SAVE_FILE = '%s/sessions.sav' % OUTPUT_DIRECTORY
SESSION_UPLOAD_FILE = '%s/to_upload_%d.sav' % OUTPUT_DIRECTORY

# Can Settings
CAN_BUS_TYPE = 'socketcan_native'
CAN_VEHICLE_CHANNEL = 'can1'
CAN_MABX_CHANNEL = 'can0'

# Logging Settings
LOG_FORMAT = '%(asctime)s => %(message)s'

# Uploader Settings
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
LOCAL_DB_NAME = 'users_db.sqlite3'
SEVER_ADDRESS = 'http://192.168.1.191:8000/'
SERVER_MAX_PING = 500  # 500 ms
SESSION_UPLOAD_FILE_FILTER = r'^upload_([0-9]+)\.txt$'
TIME_BETWEEN_UPLOAD = 300  # 5 min


# Nfc settings
GPIO_AUTHORISATION_OUTPUT = 12  # Free GPIO : 12 16 18 19 20 21 23


class MODE(Enum):
    MANUAL_DRIVING = 'MAN'
    COOPERATIVE_DRIVING = 'COP'
    AUTONOMOUS_DRIVING = 'AUT'
    UNKNOWN = 'UKN'


class STATUS_CODE(Enum):
    LOGIN = 1
    LOGOUT = 2


# Load local settings
try:
    from local_settings import *
except ImportError:
    pass
