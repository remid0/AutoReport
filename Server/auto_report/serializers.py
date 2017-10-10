from rest_framework import serializers
from auto_report.models import User, GpsPoint, Session


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('card_hash', 'id', 'is_autorized_to_change_mode')
        read_only_fields = ('card_hash', 'id', 'is_autorized_to_change_mode')


class GpsPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = GpsPoint
        fields = ('datetime', 'latitude', 'longitude', 'altitude')


class SessionSerializer(ModelSerializer):

    gps_traces = GpsPointSerializer(many=True)

    class Meta:
        model = Session
        fields = ('distance', 'gps_traces', 'mode', 'start_date', 'stop_date', 'users')

    def create(self, validated_data):
        gps_traces = validated_data.pop('gps_traces')
        users = validated_data.pop('users')
        session = Session.objects.create(**validated_data)
        for gps_trace in gps_traces:
            GpsPoint.objects.create(session=session, **gps_trace)
        session.users.add(*users)
        self.create_roads(session)
        return session

    def create_roads(self, session):
        # TODO : create roads here
        # Put some code here instead of pass
        pass
