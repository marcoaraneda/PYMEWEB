from django.db import models
from apps.stores.models import Store


class Page(models.Model):
    HOME = "HOME"
    ABOUT = "ABOUT"              # Nosotros
    FACILITIES = "FACILITIES"    # Instalaciones

    PAGE_TYPES = [
        (HOME, "Home"),
        (ABOUT, "Nosotros"),
        (FACILITIES, "Instalaciones"),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="pages")
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES)
    title = models.CharField(max_length=150, blank=True)
    content = models.TextField(blank=True)

    is_published = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("store", "page_type")

    def __str__(self):
        return f"{self.store.slug} - {self.page_type}"


class HomeSection(models.Model):
    # Secciones predefinidas (más robusto que un builder libre)
    HERO = "HERO"
    CATEGORIES = "CATEGORIES"
    FEATURED_PRODUCTS = "FEATURED_PRODUCTS"
    ABOUT_SNIPPET = "ABOUT_SNIPPET"
    FACILITIES_SNIPPET = "FACILITIES_SNIPPET"
    FAQ_SNIPPET = "FAQ_SNIPPET"
    CONTACT_SNIPPET = "CONTACT_SNIPPET"

    SECTION_TYPES = [
        (HERO, "Hero principal"),
        (CATEGORIES, "Categorías destacadas"),
        (FEATURED_PRODUCTS, "Productos destacados"),
        (ABOUT_SNIPPET, "Resumen Nosotros"),
        (FACILITIES_SNIPPET, "Resumen Instalaciones"),
        (FAQ_SNIPPET, "Preguntas frecuentes"),
        (CONTACT_SNIPPET, "Contacto"),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="home_sections")
    section_type = models.CharField(max_length=40, choices=SECTION_TYPES)

    enabled = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    # Configuración flexible por sección (texto, colores, imágenes, links)
    config = models.JSONField(default=dict, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("store", "section_type")
        ordering = ["order"]

    def __str__(self):
        return f"{self.store.slug} - {self.section_type}"
