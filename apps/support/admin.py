from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "store", "status", "priority", "created_by", "created_at")
    list_filter = ("status", "priority", "store")
    search_fields = ("title", "description", "store__slug", "created_by__username")
