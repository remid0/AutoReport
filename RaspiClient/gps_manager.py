import os

from gps3.agps3threaded import AGPS3mechanism


class GpsManager(object):

    def __init__(self):
        os.system('sudo gpsd /dev/ttyUSB0')
        self.agps_thread = AGPS3mechanism()
        self.agps_thread.stream_data()
        self.agps_thread.run_thread()

    def get_gps_point(self):
        # TODO : check time and raise error if needed
        return {
            'alt': self.agps_thread.data_stream.alt,
            'lat': self.agps_thread.data_stream.lat,
            'lon': self.agps_thread.data_stream.lon,
            'speed': self.agps_thread.data_stream.speed,
            'time': self.agps_thread.data_stream.time,
            'track': self.agps_thread.data_stream.track
        }
