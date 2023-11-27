from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import User
from django.utils.translation import gettext_lazy as _
from .models import UserProxy
from django.utils import timezone


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    'is_deleted',
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", 'update_user', 'deleted_at')}),
    )
    readonly_fields =('date_joined', 'last_login', 'update_user', 'is_deleted', 'deleted_at')
    list_display_links = ('username', 'email')
    actions = ('deleted_user',)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).filter(is_deleted=False)
    
    def deleted_user(self, request, queryset):
        queryset.update(is_deleted=True, deleted_at=timezone.now(), is_active=False)


@admin.register(UserProxy)
class UserProxyAdmin(admin.ModelAdmin):
    list_display_links = ('username', 'email')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_deleted', 'deleted_at')
    actions = ('recovery_user',)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).filter(is_deleted=True)
    
    def recovery_user(self, request, queryset):
        queryset.update(is_deleted=False, is_active=True, deleted_at=None)
        