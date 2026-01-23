from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.stores.models import Store
from apps.catalogo.models import Category


DEFAULT_CATEGORIES = [
    "Tecnologia",
    "Telefonia",
    "TV y Audio",
    "Computadores",
    "Tablets",
    "Consolas y Videojuegos",
    "Accesorios Tech",
    "Electrodomesticos",
    "Refrigeracion",
    "Cocina",
    "Lavado y Planchado",
    "Climatizacion",
    "Hogar",
    "Muebles",
    "Dormitorio",
    "Bano",
    "Deco e Iluminacion",
    "Organizacion",
    "Ferreteria",
    "Automotriz",
    "Deportes",
    "Fitness",
    "Camping y Aire Libre",
    "Moda Mujer",
    "Moda Hombre",
    "Moda Infantil",
    "Calzado Mujer",
    "Calzado Hombre",
    "Bebes",
    "Juguetes",
    "Belleza",
    "Cuidado Personal",
    "Salud",
    "Supermercado",
    "Alimentos",
    "Lacteos",
    "Bebidas",
    "Limpieza",
    "Mascotas",
    "Papeleria y Oficina",
    "Libreria y Libros",
]


class Command(BaseCommand):
    help = "Crea categorías base para todas las tiendas activas si no existen"

    def handle(self, *args, **options):
        created_total = 0
        for store in Store.objects.filter(is_active=True):
            for name in DEFAULT_CATEGORIES:
                slug = slugify(name)
                obj, created = Category.objects.get_or_create(
                    store=store, slug=slug, defaults={"name": name, "order": 0}
                )
                if created:
                    created_total += 1
        self.stdout.write(self.style.SUCCESS(f"Categorías creadas: {created_total}"))
