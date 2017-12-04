import logging
from multiprocessing import Process
import queue

from can.interface import Bus

from models import AutoReportException
import settings


class MABXCanReceiver(Process):

    def __init__(self, session_manager, odometer, vin):
        super(MABXCanReceiver, self).__init__()
        self.session_manager = session_manager
        self.odometer = odometer
        self.vin = vin

    def run(self):
        mabx_bus = Bus(channel=settings.CAN_MABX_CHANNEL, bustype=settings.CAN_BUS_TYPE)
        mode = None
        while True:
            message = mabx_bus.recv()

            if message.arbitration_id == 0xC1:
                new_mode = self.decode_mode_value(message.data)
                logging.info('CanManager : mode received = ' + str(new_mode))

                if mode != new_mode and new_mode != settings.MODE.UNKNOWN:
                    if mode is None:
                        if self.odometer.value == 0:
                            continue
                        self.session_manager.start_session(mode=new_mode, car=self.vin.get())
                        mode = new_mode
                    else:
                        self.session_manager.change_mode(new_mode)
                        mode = new_mode

    def decode_mode_value(self, data):
        mask = 0xF000000
        value = (int.from_bytes(data, byteorder='big') & mask) >> 24
        return self.get_mode_trigram(value)

    def get_mode_trigram(self, mode):
        return {
            2: settings.MODE.MANUAL_DRIVING.value,
            5: settings.MODE.AUTONOMOUS_DRIVING.value,
            8: settings.MODE.COOPERATIVE_DRIVING.value
        }.get(mode, settings.MODE.UNKNOWN.value)


class VehicleCanReceiver(Process):

    def __init__(self, session_manager, odometer, vin):
        super(VehicleCanReceiver, self).__init__()
        self.odometer = odometer
        self.session_manager = session_manager
        self.vin = vin

    def run(self):
        vehicle_bus = Bus(channel=settings.CAN_VEHICLE_CHANNEL, bustype=settings.CAN_BUS_TYPE)
        last_gps_odom = None
        while True:
            message = vehicle_bus.recv()

            if message.arbitration_id == 0x5D7:
                new_odometer_value = self.decode_odometer_value(message.data)
                logging.info('CanManager : odometer received = ' + str(new_odometer_value))
                self.odometer.value = new_odometer_value

                if last_gps_odom is None or (new_odometer_value - last_gps_odom) >= 1:
                    try:
                        self.session_manager.add_gps_point()
                    except AutoReportException:
                        pass
                    else:
                        last_gps_odom = new_odometer_value
                        logging.info('CanManager : gps_point added.')

            elif message.arbitration_id == 0x69F:
                logging.info('CanManager : vin received = ' + str(self.decode_vin_value(message.data)))
                try:
                    self.vin.put_nowait(self.decode_vin_value(message.data))
                except queue.Full:
                    pass

    def decode_odometer_value(self, data):
        mask = 0xFFFFF000
        return (int.from_bytes(data, byteorder='big') & mask) >> 12

    def decode_vin_value(self, data):
        # white_zoe_vin = 411332767, grey_zoe_vin = 142897311
        return int.from_bytes(data, byteorder='big')


class CanManager(object):

    def __init__(self, session_manager, odometer, vin):
        self.mabx_process = MABXCanReceiver(session_manager, odometer, vin)
        self.mabx_process.start()
        self.vehicle_process = VehicleCanReceiver(session_manager, odometer, vin)
        self.vehicle_process.start()

    def __del__(self):
        self.mabx_process.terminate()
        self.vehicle_process.terminate()
