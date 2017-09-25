from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

import ldap


class AutoReportModel(models.Model):
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(blank=True)

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

    utc_uid = models.CharField(unique=True, max_length=8, validators=[MinLengthValidator(8)])
    card_hash = models.BinaryField()
    is_autorized_to_change_mode = models.BooleanField()

    is_ldap_completed = models.BooleanField(default=False, blank=True)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    email = models.EmailField(blank=True)
    role = models.CharField(max_length=20, blank=True)

    def _prepopulate_fields(self):
        if not self.is_ldap_completed:
            connection = ldap.initialize('ldap://ldap.utc.fr:389')
            connection.set_option(ldap.OPT_NETWORK_TIMEOUT, 10.0)
            try:
                result = connection.search_s(
                    'ou=people,dc=utc,dc=fr',
                    ldap.SCOPE_ONELEVEL, "(uid=%s)" % self.utc_uid
                )
                self.first_name = result[0][1]['givenName'][0].decode('unicode_escape')
                self.last_name = result[0][1]['sn'][0].decode('unicode_escape')
                self.email = result[0][1]['mail'][0].decode('unicode_escape')
                self.role = result[0][1]['ou'][0].decode('unicode_escape')
                self.is_ldap_completed = True
            except ldap.LDAPError:
                pass

        super(User, self)._prepopulate_fields()

    def __repr__(self):

        if self.is_ldap_completed:
            return 'User : %s %s' % (self.last_name, self.first_name)
        else:
            return 'User : %s' % self.utc_uid

    def __str__(self):
        return repr(self)


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

    def __repr__(self):
        return 'Session'

    def __str__(self):
        return repr(self)
