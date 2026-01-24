from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views_public import MarketplaceSubmissionViewSet, MarketplaceProductListAPIView

router = DefaultRouter()
router.register(r"submissions", MarketplaceSubmissionViewSet, basename="marketplace-submissions")

urlpatterns = [
    path("products/", MarketplaceProductListAPIView.as_view(), name="marketplace-products"),
    path("", include(router.urls)),
]
