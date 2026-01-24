from rest_framework import serializers
from cloudinary import uploader
from .models import Product, ProductImage


class ProductAdminSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    submitted_by_name = serializers.SerializerMethodField(read_only=True)

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
            "submitted_by_name",
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

    def get_submitted_by_name(self, obj):
        user = getattr(obj, "submitted_by", None)
        if not user:
            return None
        if hasattr(user, "get_full_name"):
            full = user.get_full_name()
            if full:
                return full
        return getattr(user, "email", None) or getattr(user, "username", None)

    def _maybe_attach_image(self, product, image_url):
        if not image_url:
            return
        try:
            result = uploader.upload(image_url, folder="products")
            ProductImage.objects.create(product=product, image=result.get("public_id"))
        except Exception:
            # Falla silenciosa; no bloquea el resto de la operación
            pass
