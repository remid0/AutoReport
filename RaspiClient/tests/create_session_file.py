from datetime import datetime

from models import GpsPoint, Session
from settings import DATETIME_FORMAT, SESSION_SAVE_FILE


# Session A
session_a = Session(mode='MAN', odometer_value=10, user=[3], car=411332767)
session_a.start_date = datetime.strptime('2017-01-01T10:00:00.000Z', DATETIME_FORMAT)
session_a.stop_date = datetime.strptime('2017-01-01T10:30:00.000Z', DATETIME_FORMAT)
session_a.distance = 5
session_a.gps_points = [
    GpsPoint(
        time='2017-01-01T10:00:00.000Z',
        lat=49.42043,
        lon=2.79502,
        alt=1,
        speed=15,
        track=26,
    ),
    GpsPoint(
        time='2017-01-01T10:06:00.000Z',
        lat=49.41271,
        lon=2.81436,
        alt=2,
        speed=20,
        track=12,
    ),
    GpsPoint(
        time='2017-01-01T10:12:00.000Z',
        lat=49.4183,
        lon=2.6944,
        alt=3,
        speed=10,
        track=56,
    ),
    GpsPoint(
        time='2017-01-01T10:18:00.000Z',
        lat=49.04851,
        lon=2.09222,
        alt=4,
        speed=5,
        track=87,
    ),
    GpsPoint(
        time='2017-01-01T10:24:00.000Z',
        lat=49.04874,
        lon=2.09101,
        alt=5,
        speed=2,
        track=34,
    ),
]
del session_a._initial_odometer_value
#session_a.save(SESSION_SAVE_FILE)

# Session B
session_b = Session(mode='COP', odometer_value=15, user=[3], car=411332767)
session_b.start_date = datetime.strptime('2017-01-01T10:30:00.000Z', DATETIME_FORMAT)
session_b.stop_date = datetime.strptime('2017-01-01T11:30:00.000Z', DATETIME_FORMAT)
session_b.distance = 10
del session_b._initial_odometer_value
#session_b.save(SESSION_SAVE_FILE)

# Session C
session_c = Session(mode='AUT', odometer_value=25, user=[4], car=142897311)
session_c.start_date = datetime.strptime('2017-01-01T11:30:00.000Z', DATETIME_FORMAT)
session_c.stop_date = datetime.strptime('2017-01-01T14:00:00.000Z', DATETIME_FORMAT)
session_c.distance = 20
del session_c._initial_odometer_value
#session_c.save(SESSION_SAVE_FILE)

sessions = [session_a, session_b, session_c]
