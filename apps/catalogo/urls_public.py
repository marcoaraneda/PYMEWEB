from django.urls import path
from .views_public import CategoryPublicListAPIView, ProductPublicListAPIView, ProductPublicDetailAPIView

urlpatterns = [
    path("categories/", CategoryPublicListAPIView.as_view(), name="categories-public"),
    path("products/", ProductPublicListAPIView.as_view(), name="products-public"),
    path("products/<slug:slug>/", ProductPublicDetailAPIView.as_view(), name="product-public-detail"),
]
