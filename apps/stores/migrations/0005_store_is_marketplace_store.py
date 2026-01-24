from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stores", "0004_store_about"),
    ]

    operations = [
        migrations.AddField(
            model_name="store",
            name="is_marketplace_store",
            field=models.BooleanField(default=False),
        ),
    ]
