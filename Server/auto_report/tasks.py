import time

from celery.utils.log import get_task_logger
from celery import task
from django.conf import settings
import requests

from auto_report.models import GpsPoint, Road, Session


logger = get_task_logger(__name__)

@task(name='create_roads')
def create_roads(session_id):
    print(session_id)
    errors = []
    gps_point_ids = Session.objects.prefetch_related(
        'gps_points'
    ).get(
        id=session_id
    ).gps_points.all().values_list('id', flat=True)

    for gps_point_id in gps_point_ids:
        gps_point = GpsPoint.objects.get(id=gps_point_id)
        # TODO: Check if the gps_point is similar to another one associated to the road in db
        request_url = settings.NOMINATIM_URL % (gps_point.latitude, gps_point.longitude)
        try:
            result = requests.get(request_url)
            if result.status_code != 200:
                raise requests.exceptions.RequestException('Nominatim requests failed')
        except requests.exceptions.RequestException as error:
            errors.append(error)
            continue

        result = result.json()
        # Name and City in result mean the road is valid
        if (
                result.get('address') and
                result['address'].get('road') and
                result['address'].get('county')
        ):
            road, created = Road.objects.update_or_create(
                name=result['address']['road'],
                city=result['address']['county'],
                defaults={'kind': result['extratags']},
            )

            gps_point.road = road
            gps_point.save()
        time.sleep(settings.NOMINATIM_SLEEP)

    if errors:
        raise errors[0]
