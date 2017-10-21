from db_manager import DBManager
from gps_manager import GpsManager
from nfc_manager import NFCManager


# Local Database initialisation
db_manager = DBManager()
db_manager.init_local_db()
# if network
db_manager.update_local_db()

# gps initialisation
gps_manager = GpsManager()

# NFC reader initialisation
nfc_manager = NFCManager()

# Can reader initialisation
##

# TODO: Algo

# Global Shared var
#    current_session

# last_gps_point = db_manager.last_gps_point()
# current_session = Session()
# current_session.start()
# current_session.gps_points.add(last_gps_point)

#    NFController behaviour when detect NFC_card
#        if no user in current_session
#            current_session.user = new_user(NFC_card)
#        else if session is MANUAL
#            current_session.close()
#            db_manager.save_session(current_session)
#            current_session = Session()
#            current_session.user = new_user(NFC_card)
#            current_session.start()

# while True:
#    if SIGKILL:  # get SIGKILL from can_manager
#        break
#    # Lot of stuff here

# Kill all process
# store last gps point in the local db
# if network: #  Consider use network manager in a sub process
#    db_manager.update_remote_db()
