from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Review
from .serializers import ReviewPublicSerializer

class ReviewPublicListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewPublicSerializer

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        product_slug = self.kwargs.get("product_slug")

        qs = Review.objects.filter(store__slug=store_slug)

        # Solo mostrar aprobadas (ajusta el valor si tu choices usa otro texto)
        qs = qs.filter(status="APPROVED")

        if product_slug:
            qs = qs.filter(product__slug=product_slug)

        return qs.order_by("-created_at")
