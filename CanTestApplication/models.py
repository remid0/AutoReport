from datetime import datetime
import pickle


class GpsPoint(object):

    def __init__(self, **kwargs):
        self.altitude = kwargs.get('alt', None)
        self.latitude = kwargs.get('lat', None)
        self.longitude = kwargs.get('lon', None)
        self.speed = kwargs.get('speed', None)
        self.datetime = kwargs.get('time', None)
        self.track = kwargs.get('track', None)

class Session(object):

    def __init__(self, mode, odometer_value, car, **kwargs):

        self.start_datetime = datetime.utcnow()
        self.mode = mode
        self.user = kwargs.get('user', None)
        self.car = car
        self.gps_points = []
        self.end_datetime = None
        self.distance = None

        self._initial_odometer_value = odometer_value

    def stop(self, odometer_value):
        self.end_datetime = datetime.utcnow()
        self.distance = odometer_value - self._initial_odometer_value
        del self._initial_odometer_value

    def save(self, filename):
        with open(filename, 'ab+') as session_save_file:
            pickle.dump(self, session_save_file)