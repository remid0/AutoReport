from datetime import datetime

from rest_framework.generics import CreateAPIView, ListAPIView

from auto_report.models import User
from auto_report.serializers import UserSerializer, GpsTraceSerializer, SessionSerializer


class CreateGpsTraceView(CreateAPIView):

    serializer_class = GpsTraceSerializer(many=True)


class UserView(ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        datetime_format = '%Y-%m-%d %H:%M:%S.%f %Z%z'
        queryset = User.objects.all()
        if 'last_update' in self.request.query_params:
            queryset = queryset.filter(updated_at__gte=datetime.strptime(
                self.request.query_params['last_update'],
                datetime_format
            ))
        return queryset
