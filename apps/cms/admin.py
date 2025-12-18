from django.contrib import admin
from .models import Page, HomeSection


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "page_type", "title", "is_published", "updated_at")
    list_filter = ("store", "page_type", "is_published")
    search_fields = ("store__slug", "title")


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "section_type", "enabled", "order", "updated_at")
    list_filter = ("store", "enabled", "section_type")
    search_fields = ("store__slug",)
    ordering = ("store", "order")
