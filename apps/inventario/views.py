from rest_framework import viewsets
from apps.usuarios.permissions import CanManageInventory
from apps.stores.models import Store
from .models import InventoryStock, StockMovement
from .serializers_admin import InventoryStockAdminSerializer, StockMovementAdminSerializer


class InventoryStockAdminViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryStockAdminSerializer
    permission_classes = [CanManageInventory]

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return InventoryStock.objects.filter(store__slug=store_slug).select_related(
            "store", "variant", "variant__product"
        )

    def perform_create(self, serializer):
        store_slug = self.kwargs["store_slug"]
        store = Store.objects.get(slug=store_slug, is_active=True)
        serializer.save(store=store)


class StockMovementAdminViewSet(viewsets.ModelViewSet):
    serializer_class = StockMovementAdminSerializer
    permission_classes = [CanManageInventory]

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return StockMovement.objects.filter(store__slug=store_slug).select_related(
            "store", "variant", "variant__product"
        )

    def perform_create(self, serializer):
        store_slug = self.kwargs["store_slug"]
        store = Store.objects.get(slug=store_slug, is_active=True)
        serializer.save(store=store)
