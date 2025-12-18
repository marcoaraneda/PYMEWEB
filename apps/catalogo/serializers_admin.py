from rest_framework import serializers
from .models import Product


class ProductAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "store", "category", "name", "slug", "description", "price", "is_active", "is_featured"]
        read_only_fields = ["store"]
