from ctypes import c_uint, c_int
from multiprocessing import Process
from multiprocessing.sharedctypes import Value

from can import Message
from can.interface import Bus


import settings

class MABXCanSender(Process):

    def __init__(self, mode):
        super(MABXCanSender, self).__init__()
        self.data = []
        self.mode = mode
        self.mabx_bus = Bus(channel=settings.CAN_MABX_CHANNEL, bustype=settings.CAN_BUS_TYPE)

    def run(self):
        while True:
            self.encode_mode_value()
            message = Message(arbitration_id=0xC1, data=self.data, extended_id=False)
            self.mabx_bus.send(message)

    def encode_mode_value(self):
        self.data = (self.mode.value << 24 ).to_bytes(5, byteorder='big')


class VehicleCanSender(Process):
    def __init__(self, odometer):
        super(VehicleCanSender, self).__init__()
        self.data = []
        self.odometer = odometer
        self.vehicle_bus = Bus(channel=settings.CAN_VEHICLE_CHANNEL, bustype=settings.CAN_BUS_TYPE)

    def run(self):
        while True:
            self.encode_odometer_value()
            message = Message(arbitration_id=0x5D7, data=self.data, extended_id=False)
            self.vehicle_bus.send(message)

    def encode_odometer_value(self):
        self.data = (self.odometer.value << 12 ).to_bytes(7, byteorder='big')


class CanManager(object):

    def __init__(self, mabxAvailable):
        self.odometer = Value(c_uint, 0)
        self.mode = Value(c_int, 2)

        if mabxAvailable:
            self.mabx_process = MABXCanSender(self.mode)
            self.mabx_process.start()

        self.vehicle_process = VehicleCanSender(self.odometer)
        self.vehicle_process.start()

    def set_odometer(self, value):
        self.odometer.value = int(value)

    def set_mode(self, trigram):
        self.mode.value = {
            settings.MODE.MANUAL_DRIVING.value : 2,
            settings.MODE.AUTONOMOUS_DRIVING.value : 5,
            settings.MODE.COOPERATIVE_DRIVING.value : 8
        }.get(trigram, 2)