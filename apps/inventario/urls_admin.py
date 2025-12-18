from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_admin import InventoryStockAdminViewSet, StockMovementAdminViewSet

router = DefaultRouter()
router.register(r"stocks", InventoryStockAdminViewSet, basename="admin-stocks")
router.register(r"movements", StockMovementAdminViewSet, basename="admin-movements")

urlpatterns = [
    path("", include(router.urls)),
]
