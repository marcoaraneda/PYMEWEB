from django.db.models import ProtectedError
from rest_framework import viewsets, status
from rest_framework.response import Response
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            # Si tiene pedidos asociados, no se elimina; se desactiva para mantener integridad.
            instance.is_active = False
            instance.save(update_fields=["is_active"])
            return Response({"detail": "El producto tiene pedidos y se ha desactivado en lugar de eliminarse."}, status=status.HTTP_200_OK)
