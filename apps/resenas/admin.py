from django.contrib import admin
from .models import Review
from apps.reportes.utils import export_as_csv



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "product", "rating", "status", "customer_name", "created_at")
    list_filter = ("store", "status", "rating")
    search_fields = ("product__name", "customer_name", "comment")
    actions = ["approve_reviews", "reject_reviews"]

@admin.action(description="Exportar seleccionadas a CSV")
def export_csv(self, request, queryset):
    fields = ["id", "rating", "status", "customer_name", "comment", "created_at"]
    return export_as_csv(self, request, queryset, fields, filename="resenas.csv")


    @admin.action(description="Aprobar reseñas seleccionadas")
    def approve_reviews(self, request, queryset):
        queryset.update(status=Review.APPROVED)

    @admin.action(description="Rechazar reseñas seleccionadas")
    def reject_reviews(self, request, queryset):
        queryset.update(status=Review.REJECTED)
