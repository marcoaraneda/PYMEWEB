from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny



class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return Category.objects.filter(
            store__slug=store_slug,
            is_active=True
        )


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return Product.objects.filter(
            store__slug=store_slug,
            is_active=True
        ).select_related("category").prefetch_related("variants")
