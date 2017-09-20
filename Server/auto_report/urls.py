from django.conf.urls import url
from auto_report import views


urlpatterns = [  # pylint: disable=invalid-name
    url(
        r'^sessions/create/$',
        views.CreateSessionsView.as_view(),
        name='create'
    ),
    url(
        r'^users/$',
        views.UserView.as_view(),
        name='get'
    ),
]
