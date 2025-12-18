from django.db import models
from apps.stores.models import Store
from apps.catalogo.models import ProductVariant


class InventoryStock(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="stocks")
    variant = models.OneToOneField(ProductVariant, on_delete=models.CASCADE, related_name="stock")

    stock_available = models.IntegerField(default=0)
    stock_minimum = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.variant} | stock={self.stock_available}"


class StockMovement(models.Model):
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    ADJUST = "ADJUST"

    MOVEMENT_TYPES = [
        (ENTRY, "Entrada"),
        (EXIT, "Salida"),
        (ADJUST, "Ajuste"),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="stock_movements")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="movements")

    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()  # positiva o negativa según regla, o solo positiva con tipo

    reason = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} {self.quantity} - {self.variant}"
