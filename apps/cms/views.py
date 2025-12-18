from rest_framework import generics
from .models import Page, HomeSection
from .serializers import PageSerializer, HomeSectionSerializer
from rest_framework.permissions import AllowAny



class HomeSectionListAPIView(generics.ListAPIView):
    serializer_class = HomeSectionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return HomeSection.objects.filter(
            store__slug=store_slug,
            enabled=True
        ).order_by("order")


class PageDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PageSerializer
    lookup_field = "page_type"
    permission_classes = [AllowAny]

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return Page.objects.filter(
            store__slug=store_slug,
            is_published=True
        )
