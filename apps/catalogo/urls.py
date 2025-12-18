from django.urls import path
from .views import CategoryListAPIView, ProductListAPIView

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="categories"),
    path("products/", ProductListAPIView.as_view(), name="products"),
]
