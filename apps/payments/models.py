# apps/payments/models.py
from django.db import models
from apps.orders.models import Order

class Payment(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    token = models.CharField(max_length=255, blank=True)
    buy_order = models.CharField(max_length=50)
    session_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        default='created'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment {self.buy_order}'
