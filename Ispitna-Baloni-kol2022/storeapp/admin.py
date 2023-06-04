from typing import Optional

from django.contrib import admin
from django.http import HttpRequest

# Register your models here.
from .models import Pilot, Company, Balloon, Flight


class FlightAdmin(admin.ModelAdmin):

    readonly_fields = ('user', )

    def has_change_permission(self, request, obj: Optional[Flight] = None):
        if obj is None:
            return False
        if obj.user == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    def save_model(self, request: HttpRequest, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", ]


class PilotAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    exclude = ('company', )


class BalloonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Flight, FlightAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Pilot, PilotAdmin)
admin.site.register(Balloon, BalloonAdmin)
