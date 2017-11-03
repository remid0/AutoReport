from ctypes import c_int
from multiprocessing.managers import BaseManager
from multiprocessing import Value

from can_manager import CanManager
from gps_manager import GpsManager
from models import AutoReportException
from nfc_manager import NFCManager
from session_manager import SessionManager


class Main():

    def __init__(self):
        pass

    def run(self):

        BaseManager.register('SessionManager', SessionManager)
        manager = BaseManager()
        manager.start()
        odometer_value = Value(c_int)
        session_manager = manager.SessionManager(odometer_value)

        try:
            session_manager.get_db_manager.update_local_db()
        except AutoReportException:  # Network Error
            pass

        can_manager = CanManager(session_manager, odometer_value)
        nfc_manager = NFCManager(session_manager)

        # join the can manager sub process and wait it to exit()

        # gps_manger.terminate (to save the last gps point)

        # upload session file and if succes delete it

if __name__ == '__main__':
    Main().run()
