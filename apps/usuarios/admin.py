from django.contrib import admin
from .models import Role, StoreMembership


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "code")
    search_fields = ("code",)


@admin.register(StoreMembership)
class StoreMembershipAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "store", "is_active", "created_at")
    list_filter = ("store", "is_active")
    search_fields = ("user__username", "user__email", "store__slug")
    filter_horizontal = ("roles",)
