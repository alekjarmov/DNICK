from django.contrib import admin
from typing import Optional

from django.http import HttpRequest

# Register your models here.
from .models import Car, WorkShop, Producer, ProducerWorkshop, Repair


class ProducerWorkshopAdmin(admin.StackedInline):
    model = ProducerWorkshop
    extra = 1


class WorkShopAdmin(admin.ModelAdmin):
    inlines = [ProducerWorkshopAdmin]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(WorkShop, WorkShopAdmin)


class RepairAdmin(admin.ModelAdmin):
    exclude = ['user']

    def save_model(self, request, obj: Repair, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Repair, RepairAdmin)


class ProducerAdmin(admin.ModelAdmin):
    list_display = ["name"]

    def has_add_permission(self, request: HttpRequest):
        return request.user.is_superuser


admin.site.register(Producer, ProducerAdmin)


class CarAdmin(admin.ModelAdmin):
    list_display = ["type", "max_speed"]


admin.site.register(Car, CarAdmin)
