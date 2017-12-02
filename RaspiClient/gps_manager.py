from multiprocessing import Lock, Process
import os
import pickle

from gps3 import agps3

from models import GpsPoint
from settings import GPS_DEVICE, LAST_GPS_POINT_FILE


class GpsProcess(Process):
    def __init__(self, lock):
        super(GpsProcess, self).__init__()
        self.file_lock = lock
        self.gpsd_socket = agps3.GPSDSocket()
        self.gpsd_socket.connect()
        self.gpsd_socket.watch()
        self.data_stream = agps3.DataStream()

    def run(self):
        for new_data in self.gpsd_socket:
            if new_data:
                self.data_stream.unpack(new_data)
                new_gps_point = GpsPoint(**self.data_stream.alt)
                if new_gps_point.latitude != 'n/a' and new_gps_point.longitude != 'n/a':
                    with self.file_lock:
                        with open(LAST_GPS_POINT_FILE, 'wb') as gps_save_file:
                            pickle.dump(new_gps_point, gps_save_file)

    def __del__(self):
        self.gpsd_socket.close()


class GpsManager(object):

    def __init__(self):
        self.file_lock = Lock()
        os.system('sudo gpsd %s' % GPS_DEVICE)

    def get_gps_point(self):
        with self.file_lock:
            with open(LAST_GPS_POINT_FILE, 'rb') as gps_save_file:
                return pickle.load(gps_save_file)

    def __del__(self):
        self.subprocess.terminate()
