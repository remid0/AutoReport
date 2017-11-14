from django.contrib import admin

from auto_report.models import Car, GpsPoint, Road, Session, User


class CarAdmin(admin.ModelAdmin):
    readonly_fields = ('updated_at',)


class GpsPointAdmin(admin.ModelAdmin):
    raw_id_fields = ['session', 'road']


class RoadAdmin(admin.ModelAdmin):
    readonly_fields = ('updated_at',)


class SessionAdmin(admin.ModelAdmin):

    raw_id_fields = ['users']
    readonly_fields = ('updated_at',)


class UserAdmin(admin.ModelAdmin):

    search_fields = ['first_name', 'last_name', 'utc_uid']
    readonly_fields = ('updated_at',)


admin.site.register(Car, CarAdmin)
admin.site.register(GpsPoint, GpsPointAdmin)
admin.site.register(Road, RoadAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(User, UserAdmin)
