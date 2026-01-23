from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

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


class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = StoreSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Lecturas públicas solo en tiendas activas; para actualizar/eliminar
        # permitimos incluir inactivas para que un admin pueda reactivar o borrar.
        if self.request.method in permissions.SAFE_METHODS:
            return Store.objects.filter(is_active=True)
        return Store.objects.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

    def _ensure_admin(self, user, slug):
        allowed_roles = [Role.ADMIN]
        if getattr(user, "is_staff", False):
            return True
        try:
            membership = StoreMembership.objects.get(user=user, store__slug=slug, is_active=True)
            if membership.roles.filter(code__in=allowed_roles).exists():
                return True
            return False
        except StoreMembership.DoesNotExist:
            return False

    def update(self, request, *args, **kwargs):
        # Solo admins de la tienda pueden actualizar branding
        if request.method not in permissions.SAFE_METHODS:
            if not self._ensure_admin(request.user, kwargs.get("slug")):
                return Response({"detail": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self._ensure_admin(request.user, kwargs.get("slug")):
            return Response({"detail": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)

        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyStoresView(generics.ListAPIView):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Store.objects.filter(
            memberships__user=self.request.user,
            memberships__is_active=True,
            is_active=True,
        ).distinct()
