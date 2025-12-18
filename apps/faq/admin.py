from django.contrib import admin
from django.utils import timezone
from .models import FAQItem, ProductQuestion
from apps.reportes.utils import export_as_csv



@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "question", "category", "order", "is_active", "created_at")
    list_filter = ("store", "is_active", "category")
    search_fields = ("question", "answer", "category")
    ordering = ("store", "order", "id")


@admin.register(ProductQuestion)
class ProductQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "product", "status", "customer_name", "created_at", "answered_at")
    list_filter = ("store", "status")
    search_fields = ("product__name", "question", "answer", "customer_name")
    actions = ["mark_answered", "hide_questions"]

    @admin.action(description="Marcar como respondida (si tiene respuesta)")
    def mark_answered(self, request, queryset):
        now = timezone.now()
        for q in queryset:
            if q.answer.strip():
                q.status = ProductQuestion.ANSWERED
                q.answered_at = now
                q.save()

    @admin.action(description="Ocultar preguntas seleccionadas")
    def hide_questions(self, request, queryset):
        queryset.update(status=ProductQuestion.HIDDEN)
        actions = ["export_csv", "mark_answered", "hide_questions"]

@admin.action(description="Exportar seleccionados a CSV")
def export_csv(self, request, queryset):
    fields = ["id", "status", "customer_name", "question", "answer", "created_at", "answered_at"]
    return export_as_csv(self, request, queryset, fields, filename="preguntas_producto.csv")

