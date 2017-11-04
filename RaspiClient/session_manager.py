from threading import RLock

from db_manager import DBManager
from gps_manager import GpsManager
from models import AutoReportException, Session
import settings
from settings import MODE, STATUS_CODE


class SessionManager():

    def __init__(self, odometer_value):
        self.odometer_value = odometer_value
        self.current_session = None
        self.db_manager = DBManager()
        self.gps_manager = GpsManager(self.db_manager)
        self.session_lock = RLock()

    def __del__(self):
        with self.session_lock:
            self.gps_manager.stop()

    def start_session(self, mode, **kwargs):
        with self.session_lock:
            self.current_session = Session(mode, self.odometer_value.value, **kwargs)

    def end_current_session(self):
        with self.session_lock:
            self.current_session.stop(self.odometer_value.value)
            self.current_session.save(settings.SESSION_SAVE_FILE)

    def add_gps_point(self, gps_point):
        with self.session_lock:
            self.current_session.gps_points.append(gps_point)

    def change_mode(self, new_mode):
        with self.session_lock:
            self.end_current_session()
            self.start_session(new_mode, user=self.current_session.user)

    def change_user(self, new_user):
        with self.session_lock:
            if self.current_session != MODE.MANUAL_DRIVING:
                raise AutoReportException('Cannot logout while autonomous driving is on')
            self.end_current_session()
            if new_user == self.current_session.user:
                self.start_session(self.current_session.mode)
                return STATUS_CODE.LOGOUT
            self.start_session(self.current_session.mode, user=new_user)
            return STATUS_CODE.LOGIN

    def get_db_manager(self):
        return self.db_manager

    def add_gpt_point(self):
        with self.session_lock:
            try:
                gps_point = self.gps_manager.get_gps_point()
            except AutoReportException:
                pass
            else:
                self.current_session.gps_points.append(gps_point)