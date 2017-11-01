from ctypes import c_uint, c_float
from datetime import datetime
from multiprocessing import Process
from multiprocessing.sharedctypes import Value

import can


class CanReceiver(object):

    @classmethod
    def receive(cls, odometer_value, odometer_time, vin, vehicule_state, vehicule_bus):
        while True:
            message = vehicule_bus.recv()

            if message.arbitration_id == 0x5D7:
                odometer_value.value = cls.decode_odometer_value(message.data)
                odometer_time.value = message.timestamp

            elif message.arbitration_id == 0x69F:
                vin.value = cls.decode_vin_value(message.data)

            elif message.arbitration_id == 0x35C:
                vehicule_state.value = cls.decode_vehicule_state_value(message.data)

    @classmethod
    def decode_odometer_value(cls, data):
        mask = 0xFFFFF000
        return (int.from_bytes(data, byteorder='big') & mask) >> 12

    @classmethod
    def decode_vin_value(cls, data):
        pass

    @classmethod
    def decode_mode_value(cls, data):
        pass

    @classmethod
    def decode_vehicule_state_value(cls, data):
        mask = 0x700000000000000
        return (int.from_bytes(data, byteorder='big') & mask) >> 56


class OdometerInfo(object):
    def __init__(self, value, timestamp):
        self.value = value
        self.datetime = datetime.utcfromtimestamp(timestamp)


class CanManager(object):
    def __init__(self, vehicule_channel, pc_channel, bus_type): # PC channel or MABX channel ?
        self.odometer_value = Value(c_uint)
        self.odometer_time = Value(c_float)
        self.vin = Value(c_uint)
        self.vehicule_state = Value(c_uint)

        vehicule_bus = can.interface.Bus(channel=vehicule_channel, bustype=bus_type)
        #pc_bus = can.interface.Bus(channel=pc_channel, bus_type=bus_type)
        receiver_process = Process(target=CanReceiver.receive, args=(
            self.odometer_value, self.odometer_time, self.vin, self.vehicule_state, vehicule_bus
        ))
        receiver_process.start()

    def get_odometer_info(self):
        return OdometerInfo(self.odometer_value.value, self.odometer_time.value)

    def get_vehicule_state(self):
        pass
        # Possible states :
            # 0 : vehicule asleep & engine stopped
            # 1 : vehicule awake & engine stopped
            # 2 : ignition ON
            # 3 : starting in progress
            # 4 : vehicule awake & engine running
