from datetime import datetime
import pickle


class GpsPoint(object):

    def __init__(self, **kwargs):
        self.alt = kwargs.get('alt', None)
        self.lat = kwargs.get('lat', None)
        self.lon = kwargs.get('lon', None)
        self.speed = kwargs.get('speed', None)
        self.time = kwargs.get('time', None)
        self.track = kwargs.get('track', None)


class Session(object):
    end_datetime = None
    distance = None

    def __init__(self, user, mode, odometer_value):
        self.start_datetime = datetime.utcnow()
        self.mode = mode
        self.user = user
        self.gps_points = []

        self._initial_odometer_value = odometer_value

    def stop(self, odometer_value):
        self.end_datetime = datetime.utcnow()
        self.distance = odometer_value - self._initial_odometer_value

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
        server_pk = kwargs.get('server_pk', None)
        card_hash = kwargs.get('card_hash', None)
        is_autorized_to_change_mode = kwargs.get('is_autorized_to_change_mode', None)
