import RPi.GPIO as GPIO
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

from models import AutoReportException
from settings import STATUS_CODE, GPIO_AUTHORISATION_OUTPUT


GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_AUTHORISATION_OUTPUT, GPIO.OUT, initial=GPIO.LOW)

GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
AUTHORIZED = [0xFF, 0x00, 0x40, 0xA2, 0x04, 0x01, 0x01, 0x02, 0x02]
LOGOUT = [0xFF, 0x00, 0x40, 0x8D, 0x04, 0x01, 0x03, 0x01, 0x03]
UNAUTHORIZED = [0xFF, 0x00, 0x40, 0x45, 0x04, 0x02, 0x01, 0x05, 0x02]
ERROR = UNAUTHORIZED


class MyObserver(CardObserver):

    def __init__(self, session_manager, db_manager):
        self.db_manager = db_manager
        self.cards = []
        self.session_manager = session_manager
        super(MyObserver, self).__init__()

    def update(self, observable, actions):
        (added_cards, removed_cards) = actions
        for card in added_cards:
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
                    GPIO.output(GPIO_AUTHORISATION_OUTPUT, GPIO.HIGH)
                    card.connection.transmit(AUTHORIZED)
                else:
                    # Authorization = False
                    GPIO.output(GPIO_AUTHORISATION_OUTPUT, GPIO.LOW)
                    card.connection.transmit(UNAUTHORIZED)

            elif result == STATUS_CODE.LOGOUT:
                # Authorization = False
                GPIO.output(GPIO_AUTHORISATION_OUTPUT, GPIO.LOW)
                card.connection.transmit(LOGOUT)

        for card in removed_cards:
            if card in self.cards:
                self.cards.remove(card)


class NFCManager(object):

    def __init__(self, session_manager, db_manager):
        self.card_monitor = CardMonitor()
        card_observer = MyObserver(session_manager, db_manager)
        self.card_monitor.addObserver(card_observer)

    def __del__(self):
        self.card_monitor.instance.deleteObservers()
        GPIO.cleanup()
