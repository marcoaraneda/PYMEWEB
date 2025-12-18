from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_admin import ReviewAdminViewSet

router = DefaultRouter()
router.register(r"reviews", ReviewAdminViewSet, basename="admin-reviews")

urlpatterns = [
    path("", include(router.urls)),
]
