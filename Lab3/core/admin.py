from typing import Union, Optional

from django.contrib import admin
from .models import Blog, Comment, BlockList, File, BlogUser
from rangefilter.filters import DateTimeRangeFilter, DateRangeFilterBuilder


# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_filter = (
        ("created_at", DateRangeFilterBuilder(title="Created at")),
    )
    list_display = ('title', 'author')
    search_fields = ('title', 'content')

    def has_view_permission(self, request, obj: Optional[Blog] = None):
        if obj is None:
            return True

        if request.user not in obj.author.blocked_users.all():
            return True

        if not BlockList.objects.filter(user=obj.author.user, blocked_user=request.user).exists():
            return True  # alternative way to do it

        return False

    def has_add_permission(self, request, obj: Optional[Blog] = None):
        return True

    def has_change_permission(self, request, obj: Optional[Blog] = None):
        if obj is None:
            return False

        if request.user.is_superuser or request.user == obj.author.user:
            return True

        return False

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return False

        if request.user == obj.author.user:
            return True

        if request.user.is_superuser:
            return True

        return False


class CommentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj: Optional[Comment] = None):
        return self.edit_delete_permission(request, obj)

    def has_change_permission(self, request, obj: Optional[Comment] = None):
        return CommentAdmin.edit_delete_permission(request, obj)

    @staticmethod
    def edit_delete_permission(request, obj: Optional[Comment] = None):
        if obj is None:
            return False

        if request.user == obj.author.user:
            return True

        if request.user.is_superuser:
            return True

        return False


class PostUserAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj: Optional[BlogUser] = None):
        if obj is None:
            return False

        if request.user == obj.user:
            return True

        if request.user.is_superuser:
            return True

        return False


class FileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(BlogUser, PostUserAdmin)
admin.site.register(File, FileAdmin)
