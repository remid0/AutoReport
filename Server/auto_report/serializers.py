from rest_framework import serializers
from auto_report.models import User, GpsPoint, Session


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('card_hash', 'id', 'is_autorized_to_change_mode')
        read_only_fields = ('card_hash', 'id', 'is_autorized_to_change_mode')


class GpsPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = GpsPoint
        fields = ('datetime', 'latitude', 'longitude', 'altitude')


class SessionSerializer(serializers.ModelSerializer):

    gps_points = GpsPointSerializer(many=True)

    class Meta:
        model = Session
        fields = ('distance', 'gps_points', 'mode', 'start_date', 'stop_date', 'users')

    def create(self, validated_data):
        gps_points = validated_data.pop('gps_points')
        users = validated_data.pop('users')
        session = Session.objects.create(**validated_data)
        for gps_point in gps_points:
            GpsPoint.objects.create(session=session, **gps_point)
        session.users.add(*users)
        self.create_roads(session)
        return session

    def create_roads(self, session):
        # TODO : create roads here
        # Put some code here instead of pass
        pass
