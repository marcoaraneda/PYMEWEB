from django.urls import path
from .views import CategoryListAPIView, ProductListAPIView, ProductDetailAPIView

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="categories"),
    path("products/", ProductListAPIView.as_view(), name="products"),
    path("products/<slug:slug>/", ProductDetailAPIView.as_view(), name="product-detail"),
]
