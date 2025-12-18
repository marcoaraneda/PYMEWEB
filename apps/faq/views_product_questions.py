from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import ProductQuestion
from .serializers_product_questions import ProductQuestionPublicSerializer

class ProductQuestionPublicListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductQuestionPublicSerializer

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        product_slug = self.kwargs["product_slug"]

        # Solo mostrar respondidas (ANSWERED)
        return ProductQuestion.objects.filter(
            store__slug=store_slug,
            product__slug=product_slug,
            status=ProductQuestion.ANSWERED
        ).order_by("-created_at")
