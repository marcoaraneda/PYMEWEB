from rest_framework import viewsets
from apps.usuarios.permissions import CanEditContent
from apps.stores.models import Store
from .models import Page, HomeSection
from .serializers_admin import PageAdminSerializer, HomeSectionAdminSerializer


class PageAdminViewSet(viewsets.ModelViewSet):
    serializer_class = PageAdminSerializer
    permission_classes = [CanEditContent]

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return Page.objects.filter(store__slug=store_slug).select_related("store")

    def perform_create(self, serializer):
        store_slug = self.kwargs["store_slug"]
        store = Store.objects.get(slug=store_slug, is_active=True)
        serializer.save(store=store)


class HomeSectionAdminViewSet(viewsets.ModelViewSet):
    serializer_class = HomeSectionAdminSerializer
    permission_classes = [CanEditContent]

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return HomeSection.objects.filter(store__slug=store_slug).select_related("store").order_by("order")

    def perform_create(self, serializer):
        store_slug = self.kwargs["store_slug"]
        store = Store.objects.get(slug=store_slug, is_active=True)
        serializer.save(store=store)
