from rest_framework.generics import CreateAPIView, ListAPIView
from auto_report.models import User
from auto_report.serializers import UserSerializer, GpsTraceSerializer, SessionSerializer


class CreateGpsTraceView(CreateAPIView):

    serializer_class = GpsTraceSerializer(many=True)


class UserView(ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        # return User.objects.filter(updated_at__gt=self.request)
        print(self.request.data)
        return User.objects.all()
