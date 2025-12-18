from rest_framework import viewsets
from apps.usuarios.permissions import CanEditContent
from apps.stores.models import Store
from .models import Product
from .serializers_admin import ProductAdminSerializer


class ProductAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ProductAdminSerializer
    permission_classes = [CanEditContent]

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return Product.objects.filter(store__slug=store_slug).select_related("category", "store")

    def perform_create(self, serializer):
        store_slug = self.kwargs["store_slug"]
        store = Store.objects.get(slug=store_slug, is_active=True)
        serializer.save(store=store)
