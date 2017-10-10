from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

from db_manager import DBManager

GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
SUCCESS = [0xFF, 0x00, 0x40, 0xA2, 0x04, 0x01, 0x01, 0x02, 0x02]
FAIL = [0xFF, 0x00, 0x40, 0x45, 0x04, 0x02, 0x01, 0x05, 0x02]
LOGOUT = [0xFF, 0x00, 0x40, 0x8D, 0x04, 0x01, 0x03, 0x01, 0x03]


class MyObserver(CardObserver):

    def __init__(self):
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
                card.connection.transmit(LOGOUT)
                self.is_current_user = ''
            else:
                self.is_current_user = card_uid
                if self.db_controller.is_autorized(card_uid):
                    card.connection.transmit(SUCCESS)
                else:
                    card.connection.transmit(FAIL)

        for card in removedcards:
            if card in self.cards:
                self.cards.remove(card)

cardmonitor = CardMonitor()
cardobserver = MyObserver()
cardmonitor.addObserver(cardobserver)

# TODO: cardmonitor.instance.deleteObservers()
