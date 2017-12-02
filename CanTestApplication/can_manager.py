from ctypes import c_uint, c_int
import logging
from multiprocessing import Process
from multiprocessing.sharedctypes import Value
import time

from can import Message, CanError
from can.interface import Bus

from settings import(
    LOCAL_BUS_TYPE,
    LOCAL_MABX_CHANNEL,
    LOCAL_VEHICLE_CHANNEL,
    MABX_LOGS_FILE,
    MODE,
    RPI_BUS_TYPE,
    RPI_FILTERS,
    RPI_MABX_CHANNEL,
    RPI_VEHICLE_CHANNEL,
    VEHICLE_LOGS_FILE
)


class MABXCanSender(Process):

    def __init__(self, mode, test_type, is_log_player):
        super(MABXCanSender, self).__init__()
        self.mode = mode
        self.is_log_player = is_log_player

        try:
            if test_type == "local":
                self.mabx_bus = Bus(channel=LOCAL_MABX_CHANNEL, bustype=LOCAL_BUS_TYPE)
            else:
                self.mabx_bus = Bus(channel=RPI_MABX_CHANNEL, can_filters=RPI_FILTERS, bustype=RPI_BUS_TYPE)
        except CanError:
            logging.warning("MABXCanSender: couldn't create the mabx bus !")

    def run(self):
        if self.is_log_player:
            self.play_log_file()
        else:
            while True:
                data = self.encode_mode_value()
                message = Message(arbitration_id=0xC1, data=data, extended_id=False)
                try:
                    self.mabx_bus.send(message)
                    time.sleep(1)
                except AttributeError:
                    logging.warning("VehicleCanSender: couldn't send the message !")
                    break

    def encode_mode_value(self):
        return (self.mode.value << 24 ).to_bytes(5, byteorder='big')

    def play_log_file(self):
        with open(MABX_LOGS_FILE, "r") as file:
            lines = file.readlines()
            for line in lines:
                words = line.split()
                arbitration_id = int(words[1], 16)
                data = [int(number, 16) for number in words[3:]]

                message = Message(arbitration_id=arbitration_id, data=data, extended_id=False)
                try:
                    self.mabx_bus.send(message)
                    time.sleep(1)
                except AttributeError:
                    logging.warning("VehicleCanSender: couldn't send the message !")
                    break


class VehicleCanSender(Process):
    def __init__(self, odometer, test_type, is_log_player):
        super(VehicleCanSender, self).__init__()
        self.odometer = odometer
        self.is_log_player = is_log_player

        try:
            if test_type == "local":
                self.vehicle_bus = Bus(channel=LOCAL_VEHICLE_CHANNEL, bustype=LOCAL_BUS_TYPE)
            else:
                self.vehicle_bus = Bus(channel=RPI_VEHICLE_CHANNEL, can_filters=RPI_FILTERS, bustype=RPI_BUS_TYPE)
        except CanError:
            logging.warning("VehicleCanSender: couldn't create the vehicle bus !")

    def run(self):
        if self.is_log_player:
            self.play_log_file()
        else:
            while True:
                data = self.encode_odometer_value()
                message = Message(arbitration_id=0x5D7, data=data, extended_id=False)
                try:
                    self.vehicle_bus.send(message)
                    time.sleep(1)
                except AttributeError:
                    logging.warning("VehicleCanSender: couldn't send the message !")
                    break

    def encode_odometer_value(self):
        return (self.odometer.value << 12 ).to_bytes(7, byteorder='big')

    def play_log_file(self):
        with open(VEHICLE_LOGS_FILE, "r") as file:
            lines = file.readlines()
            for line in lines:
                words = line.split()
                arbitration_id = int(words[1], 16)
                data = [int(number, 16) for number in words[3:]]

                message = Message(arbitration_id=arbitration_id, data=data, extended_id=False)
                try:
                    self.vehicle_bus.send(message)
                    time.sleep(1)
                except AttributeError:
                    logging.warning("VehicleCanSender: couldn't send the message !")
                    break


class CanManager(object):

    def __init__(self, mabx_ready, vehicle_ready, test_type):
        self.mabx_ready = mabx_ready
        self.vehicle_ready = vehicle_ready
        self.test_type = test_type
        self.odometer = Value(c_uint, 45987)
        self.mode = Value(c_int, 2)
        self.mabx_log_playing = False
        self.vehicle_log_playing = False

        if self.mabx_ready:
            self.mabx_process = MABXCanSender(self.mode, self.test_type, False)
            self.mabx_process.start()

        if self.vehicle_ready:
           self.vehicle_process = VehicleCanSender(self.odometer, self.test_type, False)
           self.vehicle_process.start()

    def set_odometer(self, value):
        self.odometer.value = int(value)

    def set_mode(self, trigram):
        self.mode.value = {
            MODE.MANUAL_DRIVING.value : 2,
            MODE.AUTONOMOUS_DRIVING.value : 5,
            MODE.COOPERATIVE_DRIVING.value : 8
        }.get(trigram, 2)

    def play_mabx_log(self):
        if not self.mabx_log_playing:
            self.mabx_log_process = MABXCanSender(self.mode, self.test_type, True)
            self.mabx_log_process.start()
            self.mabx_log_playing = True

    def play_vehicle_log(self):
        if not self.vehicle_log_playing:
            self.vehicle_log_process = VehicleCanSender(self.mode, self.test_type, True)
            self.vehicle_log_process.start()
            self.vehicle_log_playing = True

    def stop_playing_mabx_log(self):
        if self.mabx_log_playing:
            self.mabx_log_process.terminate()
            self.mabx_log_playing = False

    def stop_playing_vehicle_log(self):
        if self.vehicle_log_playing:
            self.vehicle_log_process.terminate()
            self.vehicle_log_playing = False

    def __del__(self):
        if self.mabx_ready:
            self.mabx_process.terminate()

        if self.vehicle_ready:
            self.vehicle_process.terminate()

        if self.mabx_log_playing:
            self.mabx_log_process.terminate()

        if self.vehicle_log_playing:
            self.vehicle_log_process.terminate()
