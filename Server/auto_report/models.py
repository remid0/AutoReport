from django.db import models
from django.utils import timezone


class AutoReportModel(models.Model):
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self._prepopulate_fields()
        super(AutoReportModel, self).save(**kwargs)

    def _prepopulate_fields(self):
        now = timezone.now()
        if not self.created_at:
            self.created_at = now
        self.updated_at = now

    class Meta:
        abstract = True


class User(AutoReportModel):

    utc_uid = models.IntegerField()
    card_hash = models.IntegerField()
    is_autorized_to_change_mode = models.BooleanField()


class GpsTrace(AutoReportModel):

    datetime = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.IntegerField()
    session = models.ForeignKey('Session', on_delete=models.CASCADE, related_name='gps_traces')


class Road(AutoReportModel):

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=20)
    gps_traces = models.ManyToManyField(GpsTrace, related_name='roads')


class Session(AutoReportModel):

    MANUAL_DRINVING = 'MAN'
    AUNONOMOUS_DRIVING = 'AUT'
    MODE_CHOICES = (
        (MANUAL_DRINVING, 'manual driving'),
        (AUNONOMOUS_DRIVING, 'autonomous driving'),
    )

    start_date = models.DateTimeField()
    stop_date = models.DateTimeField()
    mode = models.CharField(max_length=3, choices=MODE_CHOICES)
    distance = models.IntegerField()
    users = models.ManyToManyField(User, related_name='sessions')
    roads = models.ManyToManyField(Road, related_name='sessions')
