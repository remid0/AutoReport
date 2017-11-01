from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

from db_manager import DBManager
from models import AutoReportException
from settings import STATUS_CODE


GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
AUTHORIZED = [0xFF, 0x00, 0x40, 0xA2, 0x04, 0x01, 0x01, 0x02, 0x02]
LOGOUT = [0xFF, 0x00, 0x40, 0x8D, 0x04, 0x01, 0x03, 0x01, 0x03]
UNAUTHORIZED = [0xFF, 0x00, 0x40, 0x45, 0x04, 0x02, 0x01, 0x05, 0x02]
ERROR = UNAUTHORIZED


class MyObserver(CardObserver):

    def __init__(self, session_manager):
        self.db_manager = DBManager()
        self.cards = []
        self.session_manager = session_manager

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            self.cards += [card]
            card.connection = card.createConnection()
            card.connection.connect()
            response, sw1, sw2 = card.connection.transmit(GET_UID)
            card_uid = toHexString(response).replace(' ', '')
            user = self.db_manager.get_user(card_uid)

            try:
                result = self.session_manager.change_user(user.server_pk)
            except AutoReportException:
                card.connection.transmit(ERROR)
                continue

            if result == STATUS_CODE.LOGIN:
                if user.is_autorized_to_change_mode:
                    # Authorization = True
                    card.connection.transmit(AUTHORIZED)
                else:
                    # Authorization = False
                    card.connection.transmit(UNAUTHORIZED)

            elif result == STATUS_CODE.LOGOUT:
                # Authorization = False
                card.connection.transmit(LOGOUT)

        for card in removedcards:
            if card in self.cards:
                self.cards.remove(card)


class NFCManager(object):

    def __init__(self, session_manager):
        self.cardmonitor = CardMonitor()
        cardobserver = MyObserver(session_manager)
        self.cardmonitor.addObserver(cardobserver)

    def __del__(self):
        self.cardmonitor.instance.deleteObservers()
