from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import render, get_object_or_404



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


    def product_detail(request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, "catalogo/product_detail.html", {
        "product": product
        })