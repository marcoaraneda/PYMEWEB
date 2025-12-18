from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import HomeSection, Page
from .serializers_public import HomeSectionPublicSerializer, PagePublicSerializer


class HomeSectionsPublicAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = HomeSectionPublicSerializer

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return HomeSection.objects.filter(
            store__slug=store_slug,
            enabled=True
        ).order_by("order", "id")


class PagePublicRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PagePublicSerializer
    lookup_field = "page_type"

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return Page.objects.filter(
            store__slug=store_slug,
            is_published=True
        )
