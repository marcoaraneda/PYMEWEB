from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryPublicListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        # Si Category tiene store:
        return Category.objects.filter(store__slug=store_slug, is_active=True).order_by("name")


class ProductPublicListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        qs = Product.objects.filter(store__slug=store_slug, is_active=True)

        category_slug = self.request.query_params.get("category")
        featured = self.request.query_params.get("featured")

        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        if featured in ("1", "true", "True"):
            qs = qs.filter(is_featured=True)

        return qs.select_related("category").prefetch_related("variants").order_by("-id")


class ProductPublicDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return Product.objects.filter(store__slug=store_slug, is_active=True).select_related("category").prefetch_related("variants")
