from rest_framework import serializers
from auto_report.models import User, GpsTrace, Session


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('utc_uid', 'card_hash', 'is_autorized_to_change_mode',)
        read_only_fields = ('utc_uid', 'card_hash', 'is_autorized_to_change_mode',)


class GpsTraceSerializer(serializers.ModelSerializer):

    class Meta:
        model = GpsTrace
        fields = ('datetime', 'latitude', 'longitude', 'altitude')


class SessionSerializer(serializers.ModelSerializer):

    users = UserSerializer(many=True)
    gps_traces = GpsTraceSerializer(many=True)

    class Meta:
        model = Session
        fields = ('start_date', 'stop_date', 'mode', 'distance', 'users', 'gps_traces')

