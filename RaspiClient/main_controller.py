from can_manager import CanManager
from db_manager import DBManager
from gps_manager import GpsManager
from nfc_manager import NFCManager
from models import Session


class MainController():

    def __init__(self):
        # TODO: define a share object current session that could be updated by NFC & CAN manager
        pass

    def run(self):
        db_manager = DBManager()
        db_manager.init_local_db()
        try:
            db_manager.update_local_db()
        except ValueError:  # Network Error
            pass
        gps_manager = GpsManager()
        nfc_manager = NFCManager()
        can_manager = CanManager()

        # This initialisation can be done in the can Manager (with current user to none)
        current_session = Session(
            user=nfc_manager.get_current_user_id(),
            mode=can_manager.get_current_mode(),
            odometer_value=can_manager.get_odometer_value()
        )
        # CanManager create new session when change mode is detected
        # NFCManager create new session when;
        #    - user log out
        #    - new user log in
        # When can manager detect SIGKILL, it trigger stop procedure

        # stop procedure
        # - kill other process if needed
        # - when killing gps-manger: store last gps point in the local db
        # - read sessions file and upload data if it's possible


if __name__ == '__main__':
    MainController().run()
