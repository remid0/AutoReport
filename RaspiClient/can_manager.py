# Fake the can manager
from multiprocessing import Process
import time


class MockCanManager(Process):

    def __init__(self, session_manager, odometer_value):
        super(MockCanManager, self).__init__()
        self.session_manager = session_manager
        self.odometer_value = odometer_value

    def run(self):
        while True:
            self.odometer_value.value = self.odometer_value.value +1
            time.sleep(1)

class CanManager(object):

    def __init__(self, session_manager, odometer_value):
        self.process = MockCanManager(session_manager, odometer_value)
        self.process.start()
