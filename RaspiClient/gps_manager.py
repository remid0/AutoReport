import os

from gps3.agps3threaded import AGPS3mechanism

from models import GpsPoint, AutoReportException
import settings


class GpsManager(object):

    def __init__(self, db_manager):
        os.system('sudo gpsd %s' % settings.GPS_DEVICE)
        self.agps_thread = AGPS3mechanism()
        self.agps_thread.stream_data()
        self.agps_thread.run_thread()

        self.db_manager = db_manager
        self.last_gps_point = self.db_manager.get_last_gps_point()

    def get_gps_point(self):
        new_gps_point = GpsPoint(
            alt=self.agps_thread.data_stream.alt,
            lat=self.agps_thread.data_stream.lat,
            lon=self.agps_thread.data_stream.lon,
            speed=self.agps_thread.data_stream.speed,
            time=self.agps_thread.data_stream.time,
            track=self.agps_thread.data_stream.track
        )
        if new_gps_point.time == self.last_gps_point.time or new_gps_point.lat == 'n/a':
            raise AutoReportException('No new value')

        self.last_gps_point = new_gps_point
        return new_gps_point

    def stop(self):
        self.db_manager.store_last_gps_point(self.last_gps_point)
