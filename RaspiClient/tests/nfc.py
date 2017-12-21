import signal
from unittest.mock import MagicMock

from models import User
from nfc_manager import NFCManager
from settings import STATUS_CODE

def main():#db_mock, session_mock):

    user = User(server_pk=3, card_hash='FEA8514E', is_authorised_to_change_mode=1)

    db_mock = MagicMock()
    db_mock.get_user.return_value = user

    session_mock = MagicMock()
    session_mock.change_user.return_value = STATUS_CODE.LOGIN



    nfc_manager = NFCManager(session_mock, db_mock)
    signal.pause()

main()