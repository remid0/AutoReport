from threading import RLock

from models import AutoReportException, Session
import settings
from settings import MODE, STATUS_CODE


class SessionManager():

    def __init__(self, odometer_value):
        self.odometer_value = odometer_value
        self.current_session = None
        self.lock = RLock()

    def start_session(self, mode, **kwargs):
        with self.lock:
            self.current_session = Session(mode, self.odometer_value.value, **kwargs)

    def end_curent_session(self):
        with self.lock:
            self.current_session.stop(self.odometer_value.value)
            self.current_session.save(settings.SESSION_SAVE_FILE)

    def add_gps_point(self, gps_point):
        with self.lock:
            self.current_session.gps_points.append(gps_point)

    def change_mode(self, new_mode):
        with self.lock:
            self.end_curent_session()
            self.start_session(new_mode, user=self.current_session.user)

    def change_user(self, new_user):
        with self.lock:
            if self.current_session != MODE.MANUAL_DRIVING:
                    raise AutoReportException('Cannot logout while autonomous driving is on')
            self.end_curent_session()
            if new_user == self.current_session.user:
                self.start_session(self.current_session.mode)
                return STATUS_CODE.LOGOUT
            self.start_session(self.current_session.mode, user=new_user)
            return STATUS_CODE.LOGIN
