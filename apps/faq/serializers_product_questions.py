from rest_framework import serializers
from .models import ProductQuestion

class ProductQuestionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuestion
        fields = ["id", "product", "question", "answer", "status", "created_at", "answered_at"]
