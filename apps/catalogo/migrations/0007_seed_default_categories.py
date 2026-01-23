from django.db import migrations

DEFAULT_CATEGORIES = [
    {"name": "Electrónica", "slug": "electronica"},
    {"name": "Ropa", "slug": "ropa"},
    {"name": "Hogar", "slug": "hogar"},
    {"name": "Deportes", "slug": "deportes"},
    {"name": "Belleza", "slug": "belleza"},
]


def seed_categories(apps, schema_editor):
    Store = apps.get_model("stores", "Store")
    Category = apps.get_model("catalogo", "Category")
    for store in Store.objects.all():
        if Category.objects.filter(store=store).exists():
            continue
        for idx, cat in enumerate(DEFAULT_CATEGORIES):
            Category.objects.create(
                store=store,
                name=cat["name"],
                slug=cat["slug"],
                order=idx,
                is_active=True,
            )


def unseed_categories(apps, schema_editor):
    Store = apps.get_model("stores", "Store")
    Category = apps.get_model("catalogo", "Category")
    slugs = [c["slug"] for c in DEFAULT_CATEGORIES]
    Category.objects.filter(slug__in=slugs, store__in=Store.objects.all()).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalogo", "0006_product_is_marketplace"),
    ]

    operations = [migrations.RunPython(seed_categories, unseed_categories)]
