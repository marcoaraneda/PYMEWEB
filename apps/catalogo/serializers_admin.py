from rest_framework import serializers
from cloudinary import uploader
from .models import Product, ProductImage


class ProductAdminSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "store",
            "category",
            "name",
            "slug",
            "description",
            "price",
            "offer_price",
            "is_active",
            "is_featured",
            "product_of_week",
            "is_marketplace",
            "image_url",
        ]
        read_only_fields = ["store"]

    def create(self, validated_data):
        image_url = validated_data.pop("image_url", None)
        product = super().create(validated_data)
        self._maybe_attach_image(product, image_url)
        return product

    def update(self, instance, validated_data):
        image_url = validated_data.pop("image_url", None)
        product = super().update(instance, validated_data)
        self._maybe_attach_image(product, image_url)
        return product

    def _maybe_attach_image(self, product, image_url):
        if not image_url:
            return
        try:
            result = uploader.upload(image_url, folder="products")
            ProductImage.objects.create(product=product, image=result.get("public_id"))
        except Exception:
            # Falla silenciosa; no bloquea el resto de la operación
            pass
