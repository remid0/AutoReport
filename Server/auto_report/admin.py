from django.contrib import admin

from auto_report.models import GpsTrace, User, Road, Session


class GpsTraceAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


class RoadAdmin(admin.ModelAdmin):
    pass


class SessionAdmin(admin.ModelAdmin):
    pass


admin.site.register(GpsTrace, GpsTraceAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Road, RoadAdmin)
admin.site.register(Session, SessionAdmin)
