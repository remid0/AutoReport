from ctypes import c_uint, c_float
from datetime import datetime
from multiprocessing import Process
from multiprocessing.sharedctypes import Value

from can.interface import Bus

import settings


class MABXCanReceiver(object):

    @classmethod
    def receive(cls, mode, mabx_bus):
        while True:
            message = mabx_bus.recv()

            if message.arbitration_id == 0xC1:
                mode.value = cls.decode_mode_value(message.data)

    @classmethod
    def decode_mode_value(cls, data):
        mask = 0xF000000
        return (int.from_bytes(data, byteorder='big') & mask) >> 24


class VehicleCanReceiver(object):

    @classmethod
    def receive(cls, odometer_value, odometer_time, vin, vehicle_state, vehicle_bus):
        while True:
            message = vehicle_bus.recv()

            if message.arbitration_id == 0x5D7:
                odometer_value.value = cls.decode_odometer_value(message.data)
                odometer_time.value = message.timestamp

            elif message.arbitration_id == 0x69F:
                vin.value = cls.decode_vin_value(message.data)

            elif message.arbitration_id == 0x35C:
                vehicle_state.value = cls.decode_vehicle_state_value(message.data)

    @classmethod
    def decode_odometer_value(cls, data):
        mask = 0xFFFFF000
        return (int.from_bytes(data, byteorder='big') & mask) >> 12

    @classmethod
    def decode_vin_value(cls, data):
        pass

    @classmethod
    def decode_vehicle_state_value(cls, data):
        mask = 0x700000000000000
        return (int.from_bytes(data, byteorder='big') & mask) >> 56


class OdometerInfo(object):
    def __init__(self, value, timestamp):
        self.value = value
        self.datetime = datetime.utcfromtimestamp(timestamp)


class CanManager(object):
    def __init__(self):
        self.odometer_value = Value(c_uint)
        self.odometer_time = Value(c_float)
        self.vin = Value(c_uint)
        self.vehicle_state = Value(c_uint)
        self.mode = Value(c_uint)

        mabx_bus = Bus(channel=settings.CAN_MABX_CHANNEL, bustype=settings.CAN_BUS_TYPE)
        vehicle_bus = Bus(channel=settings.CAN_VEHICLE_CHANNEL, bustype=settings.CAN_BUS_TYPE)

        mabx_process = Process(target=MABXCanReceiver.receive, args=(self.mode, mabx_bus))
        mabx_process.start()
        vehicle_process = Process(target=VehicleCanReceiver.receive, args=(
            self.odometer_value, self.odometer_time, self.vin, self.vehicle_state, vehicle_bus
        ))
        vehicle_process.start()

    def get_odometer_info(self):
        return OdometerInfo(self.odometer_value.value, self.odometer_time.value)

    def get_vehicle_state(self):
        pass
        # Possible states :
            # 0 : vehicle asleep & engine stopped
            # 1 : vehicle awake & engine stopped
            # 2 : ignition ON
            # 3 : starting in progress
            # 4 : vehicle awake & engine running

