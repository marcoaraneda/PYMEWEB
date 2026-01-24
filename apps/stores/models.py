from django.db import models

# Create your models here.
from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=80, unique=True)
    is_active = models.BooleanField(default=True)

    # Branding básico
    logo_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    about = models.TextField(blank=True)

    # Opcional (útil después)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.slug})"
