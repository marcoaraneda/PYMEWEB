from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .serializers_admin import ReviewAdminSerializer


class OwnerReviewsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewAdminSerializer

    def get_queryset(self):
        user = self.request.user
        return (
            Review.objects.filter(product__submitted_by=user)
            .select_related("product", "store")
            .order_by("-created_at")
        )
