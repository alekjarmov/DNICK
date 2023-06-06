from django.contrib import admin
from django.http import HttpRequest
from typing import Optional
from .models import Product, ProductSale, Category, Client, Sale


# Register your models here.
class ProductAdmin(admin.ModelAdmin):

    def save_model(self, request: HttpRequest, obj: Product, form, change) -> None:
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        if obj is None:
            return False

        return obj.user == request.user


admin.site.register(Product, ProductAdmin)


class ProductInline(admin.StackedInline):
    model = Product
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [ProductInline]

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        if obj is None:
            return False

        return request.user.is_superuser


admin.site.register(Category, CategoryAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]

admin.site.register(Client, ClientAdmin)

admin.site.register(Sale)
admin.site.register(ProductSale)
