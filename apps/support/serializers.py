from rest_framework import serializers
from apps.stores.models import Store
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    store = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Store.objects.all(),
        required=False,
        allow_null=True,
    )
    created_by_name = serializers.SerializerMethodField()
    store_slug = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "store",
            "store_slug",
            "title",
            "description",
            "status",
            "priority",
            "created_at",
            "updated_at",
            "created_by",
            "created_by_name",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by", "created_by_name", "store_slug"]

    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_username()
        return None

    def get_store_slug(self, obj):
        return obj.store.slug if obj.store else None

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["created_by"] = request.user
        return super().create(validated_data)
