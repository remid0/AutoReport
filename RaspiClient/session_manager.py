import logging
from threading import Lock, RLock

from gps_manager import GpsManager
from models import AutoReportException, Session
from settings import MODE, SESSION_SAVE_FILE, STATUS_CODE


class SessionManager(object):

    def __init__(self, odometer_value):
        self.odometer_value = odometer_value
        self.current_session = None
        self.gps_manager = GpsManager()
        self.session_lock = RLock()
        self.file_lock = Lock()

    def __del__(self):
        with self.session_lock:
            self.gps_manager.stop()

    def start_session(self, mode, car, **kwargs):
        with self.session_lock:
            self.current_session = Session(
                mode=mode,
                odometer_value=self.odometer_value.value,
                car=car,
                **kwargs
            )
        logging.info("SessionManager : start session")

    def end_current_session(self):
        with self.session_lock:
            self.current_session.stop(self.odometer_value.value)
            with self.file_lock:
                self.current_session.save(SESSION_SAVE_FILE)

    def change_mode(self, new_mode):
        with self.session_lock:
            self.end_current_session()
            self.start_session(
                mode=new_mode,
                car=self.current_session.car,
                user=self.current_session.user
            )
        logging.info("SessionManager : change mode = " + str(new_mode))

    # new_user must be given as an server user primary key 'server_pk' (integer)
    def change_user(self, new_user):
        with self.session_lock:
            if self.current_session.user is None:
                raise AutoReportException('Can Manager not Ready')
            if self.current_session.mode != MODE.MANUAL_DRIVING:
                raise AutoReportException('Cannot logout while autonomous driving is on')
            self.end_current_session()
            if new_user == self.current_session.user:
                self.start_session(mode=self.current_session.mode, car=self.current_session.car)
                return STATUS_CODE.LOGOUT
            self.start_session(
                mode=self.current_session.mode,
                user=new_user,
                car=self.current_session.car
            )
            return STATUS_CODE.LOGIN

    def add_gps_point(self):
        with self.session_lock:
            try:
                gps_point = self.gps_manager.get_gps_point()
            except AutoReportException:
                pass
            else:
                self.current_session.gps_points.append(gps_point)

    def acquire_file(self):
        self.file_lock.acquire()

    def release_file(self):
        self.file_lock.release()
