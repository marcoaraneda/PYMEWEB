from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogo", "0004_alter_productimage_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="offer_price",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="product_of_week",
            field=models.BooleanField(default=False),
        ),
    ]
