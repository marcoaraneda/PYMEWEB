from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_admin import PageAdminViewSet, HomeSectionAdminViewSet

router = DefaultRouter()
router.register(r"pages", PageAdminViewSet, basename="admin-pages")
router.register(r"home-sections", HomeSectionAdminViewSet, basename="admin-home-sections")

urlpatterns = [
    path("", include(router.urls)),
]
