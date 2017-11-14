from datetime import datetime

from django.utils import timezone
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import status
from rest_framework.response import Response

from auto_report.models import User
from auto_report.serializers import UserSerializer, SessionSerializer


class UserView(ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        queryset = User.objects.all()
        if 'last_update' in self.request.query_params:
            queryset = queryset.filter(updated_at__gte=datetime.strptime(
                self.request.query_params['last_update'],
                datetime_format
            ).replace(tzinfo=timezone.utc))
        return queryset


class CreateSessionsView(CreateAPIView):

    serializer_class = SessionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
