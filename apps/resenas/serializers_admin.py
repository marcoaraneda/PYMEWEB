from rest_framework import serializers
from .models import Review


class ReviewAdminSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "store",
            "product",
            "rating",
            "comment",
            "customer_name",
            "status",
            "created_at",
        ]
        read_only_fields = ["store", "created_at"]

    def get_product(self, obj):
        p = obj.product
        if not p:
            return None
        return {"id": p.id, "name": getattr(p, "name", ""), "slug": getattr(p, "slug", None)}
