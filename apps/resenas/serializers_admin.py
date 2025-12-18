from rest_framework import serializers
from .models import Review


class ReviewAdminSerializer(serializers.ModelSerializer):
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
