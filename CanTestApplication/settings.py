from enum import Enum

# General parameters
INITIAL_TEST_TYPE = "local"
IS_MABX_READY = True
IS_VEHICLE_READY = True
MABX_LOGS_FILE = 'logs/can_mabx.txt'
MAX_ODOMETER_VALUE = 1048574
VEHICLE_LOGS_FILE = 'logs/can_vehicle.txt'

# Parameters specific to tests on the Raspberry Pi
#TODO: change the following
RPI_APPLICATION_PATH = ''
RPI_BUS_TYPE = 'kvaser'
RPI_VEHICLE_CHANNEL = 0
RPI_MABX_CHANNEL = 1
RPI_FILTERS = None
#TODO: change the two following paths
#RPI_REMOTE_SESSIONS_FILE = '/home/pi/workspace/AutoReport/RaspiClient/output/sessions.sav'
RPI_REMOTE_SESSIONS_FILE = '/home/pi/workspace/delete_me/output/sessions.sav'
RPI_LOCAL_SESSIONS_FILE = '/home/robotex/AutoReport/sessions.sav'
RPI_ID = 'pi@192.168.147.128'

# Parameters specific to local tests
LOCAL_APPLICATION_PATH= '../RaspiClient/main.py'
LOCAL_BUS_TYPE = 'socketcan_native'
LOCAL_VEHICLE_CHANNEL = 'vcan0'
LOCAL_MABX_CHANNEL = 'vcan1'
LOCAL_SESSIONS_FILE = '../RaspiClient/output/sessions.sav'

class MODE(Enum):
    MANUAL_DRIVING = 'MAN'
    COOPERATIVE_DRIVING = 'COP'
    AUTONOMOUS_DRIVING = 'AUT'
