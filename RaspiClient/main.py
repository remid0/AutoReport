from ctype import c_int
from multiprocessing.managers import BaseManager
from multiprocessing import Value

from can_manager import CanManager
from db_manager import DBManager
from gps_manager import GpsManager
from models import AutoReportException
from nfc_manager import NFCManager
from session_manager import SessionManager


class Main():

    def __init__(self):
        pass

    def run(self):
        db_manager = DBManager()
        db_manager.init_local_db()
        try:
            db_manager.update_local_db()
        except AutoReportException:  # Network Error
            pass

        BaseManager.register('SessionManager', SessionManager)
        manager = BaseManager()
        manager.start()
        odometer_value = Value(c_int)
        session_manager = manager.SessionManager(odometer_value)

        can_manager = CanManager(session_manager, odometer_value)
        nfc_manager = NFCManager(session_manager)
        gps_manager = GpsManager()

        # join the can manager sub process and wait it to exit()

        # gps_manger.terminate (to save the last gps point)

        # upload session file and if succes delete it

if __name__ == '__main__':
    Main().run()
