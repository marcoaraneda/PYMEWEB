from django.utils.text import slugify
from rest_framework import serializers

from .models import Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "slug", "is_active", "logo_url"]
        read_only_fields = ["is_active"]

    def create(self, validated_data):
        base_slug = validated_data.get("slug") or slugify(validated_data.get("name", ""))
        slug = base_slug or "store"

        # Garantiza unicidad incrementando sufijo si existe.
        counter = 1
        while Store.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        validated_data["slug"] = slug
        return super().create(validated_data)