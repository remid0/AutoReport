from django.conf.urls import url
from auto_report import views


urlpatterns = [  # pylint: disable=invalid-name
    url(
        r'^gps_trace/create/$',
        views.CreateGpsTraceView.as_view(),
        name='create'
    ),
    url(
        r'^users/$',
        views.UserView.as_view(),
        name='get'
    ),
]
