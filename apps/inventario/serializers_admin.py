from rest_framework import serializers
from .models import InventoryStock, StockMovement


class InventoryStockAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryStock
        fields = ["id", "store", "variant", "stock_available", "stock_minimum", "updated_at"]
        read_only_fields = ["store", "updated_at"]


class StockMovementAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ["id", "store", "variant", "movement_type", "quantity", "reason", "created_at"]
        read_only_fields = ["store", "created_at"]
