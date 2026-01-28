from rest_framework import serializers
from apps.stores.models import Store
from .models import Category, Product, ProductVariant, ProductImage


class StoreLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "slug"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductVariantSerializer(serializers.ModelSerializer):
    stock_available = serializers.SerializerMethodField()
    stock_minimum = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ["id", "name", "sku", "is_active", "stock_available", "stock_minimum"]

    def get_stock_available(self, obj):
        stock = getattr(obj, "stock", None)
        return stock.stock_available if stock else 0

    def get_stock_minimum(self, obj):
        stock = getattr(obj, "stock", None)
        return stock.stock_minimum if stock else 0


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = ["id", "image", "order"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    store = StoreLiteSerializer(read_only=True)
    store_is_marketplace = serializers.SerializerMethodField()
    submitted_by_name = serializers.SerializerMethodField()
    stock_available = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "offer_price",
            "is_featured",
            "product_of_week",
            "is_marketplace",
            "store_is_marketplace",
            "submitted_by_name",
            "store",
            "category",
            "variants",
            "images",
            "stock_available",
        ]

    def get_store_is_marketplace(self, obj):
        return bool(getattr(obj.store, "is_marketplace_store", False))

    def get_submitted_by_name(self, obj):
        user = getattr(obj, "submitted_by", None)
        if not user:
            return None
        if hasattr(user, "get_full_name"):
            full = user.get_full_name()
            if full:
                return full
        return getattr(user, "email", None) or getattr(user, "username", None)

    def get_stock_available(self, obj):
        total = 0
        for variant in obj.variants.all():
            stock = getattr(variant, "stock", None)
            total += stock.stock_available if stock else 0
        return total


class MarketplaceSubmissionSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    submitted_by_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "offer_price",
            "is_active",
            "is_marketplace",
            "submitted_by_name",
            "image_url",
        ]
        read_only_fields = ["is_marketplace", "slug"]

    def get_submitted_by_name(self, obj):
        user = getattr(obj, "submitted_by", None)
        if not user:
            return None
        if hasattr(user, "get_full_name"):
            full = user.get_full_name()
            if full:
                return full
        return getattr(user, "email", None) or getattr(user, "username", None)

    def _generate_slug(self, base_slug: str, store) -> str:
        from django.utils.text import slugify

        base = slugify(base_slug) or "producto"
        slug = base
        counter = 1
        while Product.objects.filter(store=store, slug=slug).exists():
            slug = f"{base}-{counter}"
            counter += 1
        return slug

    def _maybe_attach_image(self, product, image_url: str | None):
        if not image_url:
            return
        from cloudinary import uploader
        try:
            result = uploader.upload(image_url, folder="products")
            ProductImage.objects.create(product=product, image=result.get("public_id"))
        except Exception:
            # Imagen opcional; no bloqueamos si falla la subida
            pass

    def create(self, validated_data):
        image_url = validated_data.pop("image_url", None)
        store = self.context["store"]
        user = self.context["user"]
        validated_data["slug"] = self._generate_slug(validated_data.get("name", ""), store)
        validated_data.setdefault("is_marketplace", True)
        validated_data.setdefault("submitted_by", user)
        product = super().create({**validated_data, "store": store})
        self._maybe_attach_image(product, image_url)
        return product
