from django.db import models
from django.conf import settings
from apps.stores.models import Store
from cloudinary.models import CloudinaryField


class Role(models.Model):
    """
    Roles disponibles en la plataforma (globales).
    El vínculo real con la tienda se hace con StoreMembership.
    """
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    INVENTORY = "INVENTORY"
    REPORTS = "REPORTS"

    ROLE_CHOICES = [
        (ADMIN, "Administrador"),
        (EDITOR, "Editor de contenido"),
        (INVENTORY, "Inventario/Bodega"),
        (REPORTS, "Reportes"),
    ]

    code = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.code


class StoreMembership(models.Model):
    """
    Un usuario puede pertenecer a muchas tiendas.
    En cada tienda puede tener uno o más roles.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="memberships")
    roles = models.ManyToManyField(Role, related_name="memberships")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "store")

    def __str__(self):
        return f"{self.user} -> {self.store.slug}"

    def has_role(self, role_code: str) -> bool:
        return self.roles.filter(code=role_code).exists()


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    avatar = CloudinaryField("avatar", folder="avatars", blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user}"
