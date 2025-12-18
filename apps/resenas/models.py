from django.db import models
from apps.stores.models import Store
from apps.catalogo.models import Product


class Review(models.Model):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (PENDING, "Pendiente"),
        (APPROVED, "Aprobada"),
        (REJECTED, "Rechazada"),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")

    rating = models.PositiveSmallIntegerField()  # 1..5
    comment = models.TextField(blank=True)

    # Para MVP: nombre libre. Luego puedes enlazar a un usuario/cliente.
    customer_name = models.CharField(max_length=120, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} - {self.rating}⭐ ({self.status})"
