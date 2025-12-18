from rest_framework.permissions import BasePermission
from apps.usuarios.models import StoreMembership, Role


def _get_store_slug_from_view(view):
    # Si en el futuro usas routers, puede venir por kwargs.
    return getattr(view, "kwargs", {}).get("store_slug")


class HasStoreRole(BasePermission):
    """
    Permission base: requiere que el usuario tenga un rol específico en la tienda store_slug.
    Uso: role_required = Role.ADMIN (por ejemplo)
    """
    role_required = None  # override en subclases

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        store_slug = _get_store_slug_from_view(view)
        if not store_slug:
            return False

        try:
            membership = StoreMembership.objects.select_related("store").get(
                user=request.user,
                store__slug=store_slug,
                is_active=True
            )
        except StoreMembership.DoesNotExist:
            return False

        if self.role_required is None:
            return True

        return membership.roles.filter(code=self.role_required).exists()


class IsStoreAdmin(HasStoreRole):
    role_required = Role.ADMIN


class CanEditContent(HasStoreRole):
    # Admin o Editor
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        store_slug = _get_store_slug_from_view(view)
        membership = StoreMembership.objects.get(user=request.user, store__slug=store_slug, is_active=True)
        return membership.roles.filter(code__in=[Role.ADMIN, Role.EDITOR]).exists()


class CanManageInventory(HasStoreRole):
    # Admin o Inventario
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        store_slug = _get_store_slug_from_view(view)
        membership = StoreMembership.objects.get(user=request.user, store__slug=store_slug, is_active=True)
        return membership.roles.filter(code__in=[Role.ADMIN, Role.INVENTORY]).exists()


class CanViewReports(HasStoreRole):
    # Admin o Reportes
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        store_slug = _get_store_slug_from_view(view)
        membership = StoreMembership.objects.get(user=request.user, store__slug=store_slug, is_active=True)
        return membership.roles.filter(code__in=[Role.ADMIN, Role.REPORTS]).exists()
