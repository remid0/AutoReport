from multiprocessing import Process

from can.interface import Bus

import settings


class MABXCanReceiver(Process):

    def __init__(self, session_manager, odometer_value):
        super(MABXCanReceiver, self).__init__()
        self.mode = None
        self.session_manager = session_manager
        self.odometer_value = odometer_value
        self.mabx_bus = Bus(channel=settings.CAN_MABX_CHANNEL, bustype=settings.CAN_BUS_TYPE)

    def run(self):
        while True:
            message = self.mabx_bus.recv()

            if message.arbitration_id == 0xC1:
                new_mode = self.decode_mode_value(message.data)

                if self.mode == None and self.odometer_value.value != 0:
                    self.session_manager.start_session(new_mode)
                    self.mode = new_mode

                elif self.mode != None and self.mode != new_mode:
                    self.session_manager.change_mode(new_mode)
                    self.mode = new_mode

    def decode_mode_value(self, data):
        mask = 0xF000000
        return (int.from_bytes(data, byteorder='big') & mask) >> 24


class VehicleCanReceiver(Process):

    def __init__(self, session_manager, odometer_value, vin):
        super(VehicleCanReceiver, self).__init__()
        self.odometer_value = odometer_value
        self.vin = vin
        self.vehicle_state = None
        self.vehicle_bus = Bus(channel=settings.CAN_VEHICLE_CHANNEL, bustype=settings.CAN_BUS_TYPE)

    def run(self):
        while True:
            message = self.vehicle_bus.recv()

            if message.arbitration_id == 0x5D7:
                self.odometer_value.value = self.decode_odometer_value(message.data)

            elif message.arbitration_id == 0x69F:
                self.vin.value = self.decode_vin_value(message.data)

            elif message.arbitration_id == 0x35C:
                self.vehicle_state = self.decode_vehicle_state_value(message.data)

    def decode_odometer_value(self, data):
        mask = 0xFFFFF000
        return (int.from_bytes(data, byteorder='big') & mask) >> 12

    def decode_vin_value(self, data):
        pass

    def decode_vehicle_state_value(self, data):
        mask = 0x700000000000000
        return (int.from_bytes(data, byteorder='big') & mask) >> 56

class CanManager(object):

    def __init__(self, session_manager, odometer_value, vin):
        mabx_process = MABXCanReceiver(session_manager, odometer_value)
        mabx_process.start()
        vehicle_process = VehicleCanReceiver(session_manager, odometer_value, vin)
        vehicle_process.start()
