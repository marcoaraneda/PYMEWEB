from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_admin import ProductAdminViewSet

router = DefaultRouter()
router.register(r"products", ProductAdminViewSet, basename="admin-products")

urlpatterns = [
    path("", include(router.urls)),
]
