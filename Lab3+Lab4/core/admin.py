from typing import Optional

from django.contrib import admin
from django.db.models import QuerySet

from .models import Post, Comment, BlockList, File, BlogUser, BlockList
from rangefilter.filters import DateTimeRangeFilter, DateRangeFilterBuilder


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_filter = (("created_at", DateRangeFilterBuilder(title="Created at")),)
    list_display = ("title", "author")
    search_fields = ("title", "content")
    readonly_fields = ("author",)

    def has_view_permission(self, request, obj: Optional[Post] = None):
        if obj is None:
            return True

        if request.user not in obj.author.blocked_users.all():
            return True

        if not BlockList.objects.filter(
            user=obj.author.user, blocked_user=request.user
        ).exists():
            return True  # alternative way to do it

        return False

    def has_add_permission(self, request, obj: Optional[Post] = None):
        return True

    def has_change_permission(self, request, obj: Optional[Post] = None):
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

    def get_queryset(self, request):
        qs: QuerySet = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # return the blogs where the current user is not blocked
        blocked_by = BlockList.objects.filter(
            blocked_user__user=request.user
        ).values_list("user", flat=True)
        return qs.exclude(author__user__in=blocked_by)

    def save_model(self, request, obj: Post, form, change):
        if not change:
            obj.author = BlogUser.objects.get(user=request.user)
        super().save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ("author",)

    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj: Optional[Comment] = None):
        if obj is None:
            return True

        if request.user not in obj.author.blocked_users.values_list("user", flat=True):
            return True

        return False

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

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = BlogUser.objects.get(user=request.user)
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        blocked = BlockList.objects.filter(user__user=request.user).values_list(
            "user", flat=True
        )
        return qs.exclude(author__user__in=blocked)


class BlogUserAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

        return False

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return False

        if request.user.is_superuser:
            return True

        return False

    def has_change_permission(self, request, obj: Optional[BlogUser] = None):
        if obj is None:
            return False

        if request.user == obj.user:
            return True

        if request.user.is_superuser:
            return True

        return False


class FileAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj: Optional[File] = None):
        if obj is None:
            return True
        if request.user.is_superuser:
            return True

        blocked_by = BlockList.objects.filter(
            blocked_user__user=request.user
        ).values_list("user", flat=True)
        if request.user not in blocked_by:
            return True

        return False

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj: Optional[File] = None):
        if obj is None:
            return False

        if request.user == obj.blog.author.user:
            return True

        if request.user.is_superuser:
            return True

        return False

    def has_delete_permission(self, request, obj: Optional[File] = None):
        if obj is None:
            return False

        if request.user == obj.blog.author.user:
            return True

        if request.user.is_superuser:
            return True

        return False


class BlockListAdmin(admin.ModelAdmin):
    readonly_fields = ("user",)
    list_display = ("blocked_user", "user")

    def save_model(self, request, obj, form, change):
        obj.user = BlogUser.objects.get(user=request.user)
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj: Optional[BlockList] = None):
        if obj and obj.user == request.user:
            return True

        return False

    def has_delete_permission(self, request, obj: Optional[BlockList] = None):
        if obj and obj.user == request.user:
            return True

        return False

    def has_view_permission(self, request, obj: Optional[BlockList] = None):
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        if obj.user.user == request.user:
            return True

        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user__user=request.user)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(BlogUser, BlogUserAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(BlockList, BlockListAdmin)
