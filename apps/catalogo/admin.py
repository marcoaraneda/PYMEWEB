from django.contrib import admin
from .models import Category, Product
from .models import Category, Product, ProductVariant

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "store", "is_active", "order", "created_at")
    list_filter = ("store", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "store", "category", "price", "is_active", "is_featured")
    list_filter = ("store", "category", "is_active", "is_featured")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "name", "sku", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("product__name", "name", "sku")
