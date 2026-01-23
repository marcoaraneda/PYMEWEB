from rest_framework import serializers
from apps.catalogo.models import Product
from .models import Review


class ReviewPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "rating", "comment", "customer_name", "status", "created_at"]
        read_only_fields = ["status", "created_at"]


class ReviewCreateSerializer(serializers.ModelSerializer):
    product_slug = serializers.SlugField(write_only=True)

    class Meta:
        model = Review
        fields = ["id", "rating", "comment", "customer_name", "product_slug"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La valoración debe estar entre 1 y 5")
        return value

    def create(self, validated_data):
        product_slug = validated_data.pop("product_slug")
        store_slug = self.context.get("store_slug")
        product = Product.objects.filter(slug=product_slug, store__slug=store_slug, is_active=True).first()
        if not product:
            raise serializers.ValidationError("Producto no encontrado en esta tienda")
        review = Review.objects.create(product=product, store=product.store, **validated_data)
        return review
