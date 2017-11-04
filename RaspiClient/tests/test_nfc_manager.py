from unittest.mock import MagicMock, patch

from RaspiClient.models import User
from RaspiClient.nfc_manager import NFCManager
from RaspiClient.settings import STATUS_CODE


class NfcManagerTest():

    @patch('db_manager.DBManager.get_user')
    @patch('session_manager.SessionManager.change_user')
    def run(self, mock1, mock2):
        session_manager = MagicMock()
        mock1.return_value = User(server_pk=1, is_autorized_to_change_mode=True)
        mock2.return_value = STATUS_CODE.LOGIN
        NFCManager(session_manager)


if __name__ == '__main__':
    NfcManagerTest().run()
