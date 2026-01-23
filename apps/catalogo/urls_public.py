from django.urls import path
from .views_public import CategoryPublicListAPIView, ProductPublicListAPIView, ProductPublicDetailAPIView
from apps.catalogo.views import ProductListAPIView

urlpatterns = [
    path("categories/", CategoryPublicListAPIView.as_view(), name="categories-public"),
    path("products/", ProductPublicListAPIView.as_view(), name="products-public"),
    path("products/<slug:slug>/", ProductPublicDetailAPIView.as_view(), name="product-public-detail"),
    path('productos/', ProductListAPIView.as_view(), name='public-product-list'),
    path('marketplace/products/', ProductPublicListAPIView.as_view(), name='marketplace-products'),
]

