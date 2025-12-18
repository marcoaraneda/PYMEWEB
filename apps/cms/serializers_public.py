from rest_framework import serializers
from .models import HomeSection, Page


class HomeSectionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSection
        fields = ["id", "section_type", "enabled", "order", "config"]


class PagePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["id", "page_type", "title", "content", "updated_at"]
