from ctypes import c_uint
from multiprocessing import Process
from multiprocessing.sharedctypes import Value

from can.interface import Bus

import settings


class MABXCanReceiver(Process):

    def __init__(self, mode):
        super(MABXCanReceiver, self).__init__()
        self.mode = mode
        self.mabx_bus = Bus(channel=settings.CAN_MABX_CHANNEL, bustype=settings.CAN_BUS_TYPE)

    def run(self):
        while True:
            message = self.mabx_bus.recv()
            if message.arbitration_id == 0xC1:
                self.mode.value = self.decode_mode_value(message.data)

    def decode_mode_value(self, data):
        mask = 0xF000000
        return (int.from_bytes(data, byteorder='big') & mask) >> 24


class VehicleCanReceiver(Process):

    def __init__(self, odometer_value, vin, vehicle_state):
        super(VehicleCanReceiver, self).__init__()
        self.odometer_value = odometer_value
        self.vin = vin
        self.vehicle_state = vehicle_state
        self.vehicle_bus = Bus(channel=settings.CAN_VEHICLE_CHANNEL, bustype=settings.CAN_BUS_TYPE)

    def run(self):
        while True:
            message = self.vehicle_bus.recv()

            if message.arbitration_id == 0x5D7:
                self.odometer_value.value = self.decode_odometer_value(message.data)

            elif message.arbitration_id == 0x69F:
                self.vin.value = self.decode_vin_value(message.data)

            elif message.arbitration_id == 0x35C:
                self.vehicle_state.value = self.decode_vehicle_state_value(message.data)

    def decode_odometer_value(self, data):
        mask = 0xFFFFF000
        return (int.from_bytes(data, byteorder='big') & mask) >> 12

    def decode_vin_value(self, data):
        pass

    def decode_vehicle_state_value(self, data):
        mask = 0x700000000000000
        return (int.from_bytes(data, byteorder='big') & mask) >> 56

class CanManager(object):
    def __init__(self):
        #TODO : adapt to the SessionManager code
        self.odometer_value = Value(c_uint)
        self.vin = Value(c_uint)
        self.vehicle_state = Value(c_uint)
        self.mode = Value(c_uint)

        mabx_process = MABXCanReceiver(self.mode)
        mabx_process.start()

        vehicle_process = VehicleCanReceiver(self.odometer_value, self.vin, self.vehicle_state)
        vehicle_process.start()

    def get_vehicle_state(self):
        pass
        # Possible states :
            # 0 : vehicle asleep & engine stopped
            # 1 : vehicle awake & engine stopped
            # 2 : ignition ON
            # 3 : starting in progress
            # 4 : vehicle awake & engine running
