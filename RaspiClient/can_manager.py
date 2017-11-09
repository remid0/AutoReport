from multiprocessing import Process

from can.interface import Bus

import settings


class MABXCanReceiver(Process):

    def __init__(self, session_manager, odometer):
        super(MABXCanReceiver, self).__init__()
        self.session_manager = session_manager
        self.odometer = odometer
        self.mode = None
        self.mabx_bus = Bus(channel=settings.CAN_MABX_CHANNEL, bustype=settings.CAN_BUS_TYPE)

    def run(self):
        while True:
            message = self.mabx_bus.recv()

            if message.arbitration_id == 0xC1:
                new_mode = self.decode_mode_value(message.data)

                if self.mode == None and self.odometer.value != 0:
                    self.session_manager.start_session(new_mode)
                    self.mode = new_mode

                elif self.mode != None and self.mode != new_mode:
                    self.session_manager.change_mode(new_mode)
                    self.mode = new_mode

    def decode_mode_value(self, data):
        mask = 0xF000000
        return (int.from_bytes(data, byteorder='big') & mask) >> 24


class VehicleCanReceiver(Process):

    def __init__(self, session_manager, odometer, vin):
        super(VehicleCanReceiver, self).__init__()
        self.odometer = odometer
        self.session_manager = session_manager
        self.vin = vin
        self.last_gps_odom = None
        self.vehicle_state = None
        self.vehicle_bus = Bus(channel=settings.CAN_VEHICLE_CHANNEL, bustype=settings.CAN_BUS_TYPE)

    def run(self):
        while True:
            message = self.vehicle_bus.recv()

            if message.arbitration_id == 0x5D7:
                new_odometer_value = self.decode_odometer_value(message.data)
                self.odometer.value = new_odometer_value

                if self.last_gps_odom == None or (new_odometer_value - self.last_gps_odom) >= settings.GPS_DISTANCE_INTERVAL:
                    self.session_manager.add_gps_point()
                    self.last_gps_odom = new_odometer_value

            elif message.arbitration_id == 0x69F:
                self.vin.value = self.decode_vin_value(message.data)

            elif message.arbitration_id == 0x35C:
                self.vehicle_state = self.decode_vehicle_state_value(message.data)

    def decode_odometer_value(self, data):
        mask = 0xFFFFF000
        return (int.from_bytes(data, byteorder='big') & mask) >> 12

    def decode_vin_value(self, data):
        # vin_white_zoe = 411332767
        # vin_grey_zoe = 142897311
        return int.from_bytes(data, byteorder='big')

    def decode_vehicle_state_value(self, data):
        mask = 0x700000000000000
        return (int.from_bytes(data, byteorder='big') & mask) >> 56

class CanManager(object):

    def __init__(self, session_manager, odometer, vin):
        mabx_process = MABXCanReceiver(session_manager, odometer)
        mabx_process.start()
        vehicle_process = VehicleCanReceiver(session_manager, odometer, vin)
        vehicle_process.start()
