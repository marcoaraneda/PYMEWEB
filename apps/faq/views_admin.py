from django.utils import timezone
from rest_framework import viewsets
from apps.usuarios.permissions import CanEditContent
from apps.stores.models import Store
from .models import FAQItem, ProductQuestion
from .serializers_admin import FAQItemAdminSerializer, ProductQuestionAdminSerializer

class FAQItemAdminViewSet(viewsets.ModelViewSet):
    serializer_class = FAQItemAdminSerializer
    permission_classes = [CanEditContent]

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return FAQItem.objects.filter(store__slug=store_slug).select_related("store").order_by("order", "id")

    def perform_create(self, serializer):
        store_slug = self.kwargs["store_slug"]
        store = Store.objects.get(slug=store_slug, is_active=True)
        serializer.save(store=store)

class ProductQuestionAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ProductQuestionAdminSerializer
    permission_classes = [CanEditContent]

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return ProductQuestion.objects.filter(store__slug=store_slug).select_related("store", "product")

    def perform_create(self, serializer):
        store_slug = self.kwargs["store_slug"]
        store = Store.objects.get(slug=store_slug, is_active=True)
        serializer.save(store=store)

    # Si cambias status a ANSWERED y viene answer, setea answered_at
    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == ProductQuestion.ANSWERED and instance.answer and instance.answered_at is None:
            instance.answered_at = timezone.now()
            instance.save(update_fields=["answered_at"])
