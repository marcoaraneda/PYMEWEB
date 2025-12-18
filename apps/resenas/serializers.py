from rest_framework import serializers
from .models import Review


class ReviewPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "rating", "comment", "customer_name", "created_at"]
