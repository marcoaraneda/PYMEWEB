from rest_framework import serializers
from .models import FAQItem, ProductQuestion

class FAQItemAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQItem
        fields = ["id", "store", "question", "answer", "category", "order", "is_active", "created_at"]
        read_only_fields = ["store", "created_at"]

class ProductQuestionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuestion
        fields = ["id", "store", "product", "question", "answer", "customer_name", "status", "created_at", "answered_at"]
        read_only_fields = ["store", "created_at", "answered_at"]
