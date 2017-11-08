from ctypes import c_uint, c_float
from datetime import datetime
from multiprocessing import Process
from multiprocessing.sharedctypes import Value

import can

#bustype = 'socketcan_native'
#channel = 'vcan0'
#bus = can.interface.Bus(channel=channel, bustype=bustype)
#msg = can.Message(arbitration_id=0x5D7, data=[0x00, 0x00, 0x00, 0x0B, 0x3A, 0x30, 0xC0], extended_id=False)
#bus.send(msg)

class CanReceiver(object):
    @classmethod
    def receive(cls, odometer_value, odometer_time, vehicule_bus):
        while(True):
            message = vehicule_bus.recv()
            if message.arbitration_id == 0x5D7:
                odometer_value.value = cls.decode_odometer_value(message.data)
                odometer_time.value = message.timestamp

    @classmethod
    def decode_odometer_value(cls, data): #passer taille payload ?
        return 6
        #décoder le message + retourner unsigned int

    @classmethod
    def decode_vin_value(cls, data):
        pass

    @classmethod
    def decode_mode_value(cls, data):
        pass
        #autonome ou manuel

    @classmethod
    def decode_is_off_value(cls, data):
        pass
        #véhicule éteint

class OdometerInfo(object):
    def __init__(self, value, timestamp):
        self.value = value
        self.datetime = datetime.utcfromtimestamp(self.odometer_time.value)


class CanManager(object):
    def __init__(self, vehicule_channel, pc_channel, bus_type): #PC channel or MABX channel ?
        self.odometer_value = Value(c_uint)
        self.odometer_time = Value(c_float)

        vehicule_bus = can.interface.Bus(channel=vehicule_channel, bustype=bus_type)
        #pc_bus = can.interface.Bus(channel=pc_channel, bus_type=bus_type)
        receiver_process = Process(target=CanReceiver.receive, args=(self.odometer_value, self.odometer_time, vehicule_bus))
        receiver_process.start()

    def get_odometer_info(self):
        return OdometerInfo(self.odometer_value.value, self.odometer_time.value)
