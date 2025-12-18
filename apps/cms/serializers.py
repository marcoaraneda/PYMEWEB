from rest_framework import serializers
from .models import Page, HomeSection


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["page_type", "title", "content"]


class HomeSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSection
        fields = ["section_type", "order", "config"]


