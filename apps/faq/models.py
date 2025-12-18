from django.db import models
from apps.stores.models import Store
from apps.catalogo.models import Product


class FAQItem(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="faqs")

    question = models.CharField(max_length=200)
    answer = models.TextField()

    category = models.CharField(max_length=80, blank=True)  # opcional, ej: "Envíos", "Pagos"
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.store.slug} - {self.question}"


class ProductQuestion(models.Model):
    PENDING = "PENDING"
    ANSWERED = "ANSWERED"
    HIDDEN = "HIDDEN"

    STATUS_CHOICES = [
        (PENDING, "Pendiente"),
        (ANSWERED, "Respondida"),
        (HIDDEN, "Oculta"),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="product_questions")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="questions")

    question = models.TextField()
    answer = models.TextField(blank=True)

    customer_name = models.CharField(max_length=120, blank=True)  # MVP
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} ({self.status})"
