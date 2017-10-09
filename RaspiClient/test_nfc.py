from smartcard.CardMonitoring import CardMonitor, CardObserver
# from smartcard.util import toHexString, toBytes


GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
SUCCESS = [0xFF, 0x00, 0x40, 0xA2, 0x04, 0x01, 0x01, 0x02, 0x02]
FAIL = [0xFF, 0x00, 0x40, 0x45, 0x04, 0x02, 0x01, 0x05, 0x02]


class MyObserver(CardObserver):

    def __init__(self):
        self.cards = []

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            self.cards += [card]
            card.connection = card.createConnection()
            card.connection.connect()
            response, sw1, sw2 = card.connection.transmit(GET_UID)
            print(response)
            if True:
                card.connection.transmit(SUCCESS)
            else:
                card.connection.transmit(FAIL)

        for card in removedcards:
            if card in self.cards:
                self.cards.remove(card)

cardmonitor = CardMonitor()
cardobserver = MyObserver()
cardmonitor.addObserver(cardobserver)

# cardmonitor.instance.deleteObservers()   