from django.contrib import admin
from .models import InventoryStock, StockMovement
from apps.reportes.utils import export_as_csv
from django.contrib import admin
from django.db.models import F

class LowStockFilter(admin.SimpleListFilter):
    title = "Stock bajo"
    parameter_name = "low_stock"

    def lookups(self, request, model_admin):
        return [("1", "Solo stock bajo")]

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(stock_available__lte=F("stock_minimum"))
        return queryset

@admin.register(InventoryStock)
class InventoryStockAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "variant", "stock_available", "stock_minimum", "updated_at")
    list_filter = ("store", LowStockFilter)
    search_fields = ("variant__product__name", "variant__name")
    actions = ["export_csv"]

@admin.action(description="Exportar seleccionados a CSV")
def export_csv(self, request, queryset):
    fields = ["id", "stock_available", "stock_minimum", "updated_at"]
    return export_as_csv(self, request, queryset, fields, filename="stocks.csv")

def get_queryset(self, request):
    qs = super().get_queryset(request)
    return qs.select_related("store", "variant", "variant__product")


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "variant", "movement_type", "quantity", "reason", "created_at")
    list_filter = ("store", "movement_type")
    search_fields = ("variant__product__name", "variant__name", "reason")


