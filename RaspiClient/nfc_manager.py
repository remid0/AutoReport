from ctypes import c_bool
from multiprocessing.sharedctypes import Value

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

from db_manager import DBManager

GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
AUTHORIZED = [0xFF, 0x00, 0x40, 0xA2, 0x04, 0x01, 0x01, 0x02, 0x02]
UNAUTHORIZED = [0xFF, 0x00, 0x40, 0x45, 0x04, 0x02, 0x01, 0x05, 0x02]
LOGOUT = [0xFF, 0x00, 0x40, 0x8D, 0x04, 0x01, 0x03, 0x01, 0x03]


class MyObserver(CardObserver):

    def __init__(self, is_autorized):
        self.is_autorized = is_autorized
        self.cards = []
        self.db_controllerh = DBManager()
        self.is_current_user = ''

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            self.cards += [card]
            card.connection = card.createConnection()
            card.connection.connect()
            response, sw1, sw2 = card.connection.transmit(GET_UID)
            card_uid = toHexString(response).replace(' ', '')
            if self.is_current_user == card_uid:  # self.db_controller.is_current_user(card_uid):
                self.is_autorized.value = False
                card.connection.transmit(LOGOUT)
                self.is_current_user = ''
            else:
                self.is_current_user = card_uid
                if self.db_controller.is_autorized(card_uid):
                    self.is_autorized.value = True
                    card.connection.transmit(AUTHORIZED)
                else:
                    self.is_autorized.value = False
                    card.connection.transmit(UNAUTHORIZED)

        for card in removedcards:
            if card in self.cards:
                self.cards.remove(card)


class NFCManager(object):

    def __init__(self):
        self.is_autorized = Value(c_bool)
        cardmonitor = CardMonitor()
        cardobserver = MyObserver(self.is_autorized)
        cardmonitor.addObserver(cardobserver)

# TODO: cardmonitor.instance.deleteObservers()
