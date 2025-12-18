from rest_framework import serializers
from .models import Page, HomeSection


class PageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["id", "store", "page_type", "title", "content", "is_published", "updated_at"]
        read_only_fields = ["store", "updated_at"]


class HomeSectionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSection
        fields = ["id", "store", "section_type", "enabled", "order", "config", "updated_at"]
        read_only_fields = ["store", "updated_at"]

        
    def validate(self, attrs):
        store = self.context["store"]
        section_type = attrs.get("section_type")

        # Si es update, permitir el mismo registro
        qs = HomeSection.objects.filter(store=store, section_type=section_type)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError(
                {"section_type": "Ya existe una sección con este section_type para esta tienda. Edita la existente (PUT) en vez de crear otra."}
            )

        return attrs

