from rest_framework import serializers
from .models import FAQItem

class FAQItemPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQItem
        fields = ["id", "question", "answer", "category", "order"]
