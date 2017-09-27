from django.contrib import admin

from auto_report.models import GpsTrace, User, Road, Session


class GpsTraceAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):

    search_fields = ['first_name', 'last_name', 'utc_uid']
    readonly_fields = ('updated_at',)


class RoadAdmin(admin.ModelAdmin):
    pass


class SessionAdmin(admin.ModelAdmin):

    raw_id_fields = ['roads', 'users']


admin.site.register(GpsTrace, GpsTraceAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Road, RoadAdmin)
admin.site.register(Session, SessionAdmin)
