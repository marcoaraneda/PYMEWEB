from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Category, Product
from apps.stores.models import Store
from apps.usuarios.models import StoreMembership, Role
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
        # Solo admin/owner/manager de la tienda o staff pueden crear
        if not self._user_can_edit(self.request.user, store_slug):
            raise PermissionDenied("No tienes permisos")
        serializer.save(store=store)

    def _user_can_edit(self, user, store_slug: str) -> bool:
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "is_staff", False):
            return True
        try:
            membership = StoreMembership.objects.get(user=user, store__slug=store_slug, is_active=True)
            return membership.roles.filter(code__in=[Role.ADMIN]).exists()
        except StoreMembership.DoesNotExist:
            return False


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsAuthenticated()]
        return [AllowAny()]

    def update(self, request, *args, **kwargs):
        store_slug = kwargs.get("store_slug")
        if not self._user_can_edit(request.user, store_slug):
            return Response({"detail": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        store_slug = kwargs.get("store_slug")
        if not self._user_can_edit(request.user, store_slug):
            return Response({"detail": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return Product.objects.filter(store__slug=store_slug).select_related("category").prefetch_related("variants")

    def _user_can_edit(self, user, store_slug: str) -> bool:
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "is_staff", False):
            return True
        try:
            membership = StoreMembership.objects.get(user=user, store__slug=store_slug, is_active=True)
            return membership.roles.filter(code__in=[Role.ADMIN]).exists()
        except StoreMembership.DoesNotExist:
            return False


    def product_detail(request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, "catalogo/product_detail.html", {
        "product": product
        })