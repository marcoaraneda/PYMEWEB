from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.stores.models import Store
from apps.stores.serializers import StoreSerializer
from apps.usuarios.models import StoreMembership, Role


# ✅ LISTADO DE TIENDAS (para la home)
class StoreListCreateView(generics.ListCreateAPIView):
    queryset = Store.objects.filter(is_active=True)
    serializer_class = StoreSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        # List público, creación requiere autenticación
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        store = serializer.save()
        if not self.request.user.is_authenticated:
            return store

        # Asignar membresía admin al creador
        admin_role, _ = Role.objects.get_or_create(code=Role.ADMIN)
        membership, _ = StoreMembership.objects.get_or_create(
            user=self.request.user, store=store, defaults={"is_active": True}
        )
        membership.roles.add(admin_role)
        return store


# ✅ DETALLE DE TIENDA (por slug)
class StoreDetailView(generics.RetrieveAPIView):
    queryset = Store.objects.filter(is_active=True)
    lookup_field = 'slug'
    serializer_class = StoreSerializer
    permission_classes = [AllowAny]


class MyStoresView(generics.ListAPIView):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Store.objects.filter(memberships__user=self.request.user, memberships__is_active=True).distinct()
