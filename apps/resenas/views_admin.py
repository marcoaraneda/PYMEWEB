from rest_framework import viewsets
from apps.usuarios.permissions import CanEditContent
from apps.stores.models import Store
from .models import Review
from .serializers_admin import ReviewAdminSerializer

class ReviewAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewAdminSerializer
    permission_classes = [CanEditContent]

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return Review.objects.filter(store__slug=store_slug).select_related("product", "store")

    def perform_create(self, serializer):
        store_slug = self.kwargs["store_slug"]
        store = Store.objects.get(slug=store_slug, is_active=True)
        serializer.save(store=store)
