from datetime import datetime
import pickle


class AutoReportException(Exception):
    pass


class GpsPoint(object):

    def __init__(self, **kwargs):
        self.alt = kwargs.get('alt', None)
        self.lat = kwargs.get('lat', None)
        self.lon = kwargs.get('lon', None)
        self.speed = kwargs.get('speed', None)
        self.time = kwargs.get('time', None)
        self.track = kwargs.get('track', None)


class Session(object):

    def __init__(self, mode, odometer_value, **kwargs):
        self.end_datetime = None
        self.distance = None
        self.start_datetime = datetime.utcnow()
        self.mode = mode
        self.user = kwargs.get('user', None)
        self.gps_points = []

        self._initial_odometer_value = odometer_value

    def stop(self, odometer_value):
        self.end_datetime = datetime.utcnow()
        self.distance = odometer_value - self._initial_odometer_value
        del self._initial_odometer_value

    def save(self, filename):
        with open(filename, 'ab+') as myfile:
            pickle.dump(self, myfile)

    @classmethod
    def load(cls, filename):
        sessions = []
        with open(filename, 'rb') as myfile:
            while True:
                try:
                    sessions.append(pickle.load(myfile))
                except EOFError:
                    break
        return sessions


class User(object):

    def __init__(self, **kwargs):
        self.server_pk = kwargs.get('server_pk', None)
        self.card_hash = kwargs.get('card_hash', None)
        self.is_authorized_to_change_mode = kwargs.get('is_authorized_to_change_mode', None)
