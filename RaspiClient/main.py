from ctypes import c_int
from multiprocessing.managers import SyncManager

from can_manager import CanManager
from db_manager import DBManager
from models import AutoReportException
from nfc_manager import NFCManager
from session_manager import SessionManager


class Main():

    def __init__(self):
        pass

    def run(self):

        SyncManager.register('SessionManager', SessionManager)
        SyncManager.register('DBManager', DBManager)
        manager = SyncManager()
        manager.start()

        db_manager = manager.DBManager()
        odometer_value = manager.Value(c_int, 0)
        vin = manager.Value(c_int, 0)
        session_manager = manager.SessionManager(db_manager, odometer_value)

        try:
            pass
            #db_manager.update_local_db()
        except AutoReportException:  # Network Error
            pass

        can_manager = CanManager(session_manager, odometer_value, vin)
        nfc_manager = NFCManager(session_manager, db_manager)

        #import time
        #time.sleep(10)

        # join the can manager sub process and wait it to exit()

        # gps_manger.terminate (to save the last gps point)

        # upload session file and if succes delete it

if __name__ == '__main__':
    Main().run()
