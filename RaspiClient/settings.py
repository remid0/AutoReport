from enum import Enum


CAN_BUS_TYPE = 'socketcan_native'
CAN_VEHICLE_CHANNEL = 'vcan0'
CAN_MABX_CHANNEL = 'vcan1'

GPS_DISTANCE_INTERVAL = 1 # In decameters
GPS_DEVICE = '/dev/ttyUSB0'

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
LOCAL_DB_NAME = 'users_db.sqlite3'
SEVER_ADDRESS = 'http://127.0.0.1:8000/'
SESSION_SAVE_FILE = 'sessions.sav'


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
    # pylint: disable=line-too-long,unused-wildcard-import,wildcard-import,wrong-import-position
    from local_settings import *
except ImportError:
    pass
