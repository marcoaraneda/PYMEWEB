from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Category, Product
from apps.stores.models import Store
from .serializers import CategorySerializer, ProductSerializer
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


class ProductListAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return Product.objects.filter(
            store__slug=store_slug,
            is_active=True
        ).select_related("category").prefetch_related("variants")

    def perform_create(self, serializer):
        store_slug = self.kwargs["store_slug"]
        store = get_object_or_404(Store, slug=store_slug, is_active=True)
        serializer.save(store=store)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return Product.objects.filter(store__slug=store_slug).select_related("category").prefetch_related("variants")


    def product_detail(request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, "catalogo/product_detail.html", {
        "product": product
        })