from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import FAQItem
from .serializers import FAQItemPublicSerializer

class FAQItemPublicListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FAQItemPublicSerializer

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return FAQItem.objects.filter(
            store__slug=store_slug,
            is_active=True
        ).order_by("order", "id")
