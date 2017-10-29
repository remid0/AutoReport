from ctypes import c_int
from multiprocessing.sharedctypes import Value

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

from db_manager import DBManager

GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
AUTHORIZED = [0xFF, 0x00, 0x40, 0xA2, 0x04, 0x01, 0x01, 0x02, 0x02]
UNAUTHORIZED = [0xFF, 0x00, 0x40, 0x45, 0x04, 0x02, 0x01, 0x05, 0x02]
LOGOUT = [0xFF, 0x00, 0x40, 0x8D, 0x04, 0x01, 0x03, 0x01, 0x03]


class MyObserver(CardObserver):

    current_user = None
    cards = []

    def __init__(self, current_user_id):
        self.db_manager = DBManager()
        self.current_user_id = current_user_id
        self.reset_current_user()

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            self.cards += [card]
            card.connection = card.createConnection()
            card.connection.connect()
            response, sw1, sw2 = card.connection.transmit(GET_UID)
            card_uid = toHexString(response).replace(' ', '')
            user = self.db_manager.get_user(card_uid)
            if self.current_user and self.current_user.server_pk == user.server_pk:
                # Authorization = False
                card.connection.transmit(LOGOUT)
                self.reset_current_user()
            else:
                self.current_user = user
                self.current_user_id.value = self.current_user.server_pk
                if self.current_user.is_autorized_to_change_mode:
                    # Authorization = True
                    card.connection.transmit(AUTHORIZED)
                else:
                    # Authorization = False
                    card.connection.transmit(UNAUTHORIZED)

        for card in removedcards:
            if card in self.cards:
                self.cards.remove(card)

    def reset_current_user(self):
        self.current_user = None
        self.current_user_id.value = -1


class NFCManager(object):

    def __init__(self):
        self.current_user_id = Value(c_int)
        cardmonitor = CardMonitor()
        cardobserver = MyObserver(self.current_user_id)
        cardmonitor.addObserver(cardobserver)

    def get_current_user_id(self):
        return self.current_user_id.value if self.current_user_id.value != -1 else None

# cardmonitor.instance.deleteObservers()
