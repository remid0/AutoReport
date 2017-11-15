from ctypes import c_int
from multiprocessing.managers import SyncManager

from can_manager import CanManager
from db_manager import DBManager
from nfc_manager import NFCManager
from session_manager import SessionManager
from upload_manager import UploadManager


class Main(object):

    def __init__(self):
        pass

    def run(self):

        SyncManager.register('SessionManager', SessionManager)
        SyncManager.register('DBManager', DBManager)
        manager = SyncManager()
        manager.start()

        db_manager = manager.DBManager()
        odometer_value = manager.Value(c_int, 0)
        vin = manager.Queue(1)
        session_manager = manager.SessionManager(db_manager, odometer_value)

        CanManager(session_manager, odometer_value, vin)
        NFCManager(session_manager, db_manager)
        UploadManager(session_manager, db_manager)


if __name__ == '__main__':
    Main().run()
