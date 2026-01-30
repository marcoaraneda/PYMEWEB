from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, MarketplaceSubmissionSerializer
from apps.stores.models import Store


class CategoryPublicListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        # Si Category tiene store:
        return Category.objects.filter(store__slug=store_slug, is_active=True).order_by("name")


class ProductPublicListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        qs = Product.objects.filter(store__slug=store_slug, is_active=True)

        category_slug = self.request.query_params.get("category")
        featured = self.request.query_params.get("featured")

        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        if featured in ("1", "true", "True"):
            qs = qs.filter(is_featured=True)

        marketplace = self.request.query_params.get("marketplace")
        if marketplace in ("1", "true", "True"):
            qs = qs.filter(is_marketplace=True)

        return (
            qs.select_related("category", "store", "submitted_by")
            .prefetch_related("variants", "images")
            .order_by("-id")
        )


class ProductPublicDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_queryset(self):
        store_slug = self.kwargs["store_slug"]
        return (
            Product.objects.filter(store__slug=store_slug, is_active=True)
            .select_related("category", "store")
            .prefetch_related("variants", "images")
        )


class MarketplaceProductListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        limit = self.request.query_params.get("limit")
        qs = (
            Product.objects.filter(is_active=True, is_marketplace=True)
            .select_related("category", "store", "submitted_by")
            .prefetch_related("variants", "images")
            .order_by("-created_at")
        )
        if limit:
            try:
                qs = qs[: int(limit)]
            except ValueError:
                pass
        return qs


def get_or_create_marketplace_store(user) -> Store:
    base_slug = f"marketplace-{user.id}"
    slug = base_slug
    counter = 1
    while Store.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    defaults = {
        "name": f"Marketplace {getattr(user, 'get_full_name', lambda: '')() or getattr(user, 'username', 'usuario')}",
        "is_active": False,
        "is_marketplace_store": True,
    }

    store, _ = Store.objects.get_or_create(slug=slug, defaults=defaults)

    # Asegura que si ya existía se marque como tienda de marketplace oculta
    if not store.is_marketplace_store:
        store.is_marketplace_store = True
        store.is_active = False
        store.save(update_fields=["is_marketplace_store", "is_active"])

    return store


class MarketplaceSubmissionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MarketplaceSubmissionSerializer

    def get_queryset(self):
        return (
            Product.objects.filter(submitted_by=self.request.user, is_marketplace=True)
            .select_related("store", "submitted_by")
            .prefetch_related("images")
            .order_by("-created_at")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["store"] = get_or_create_marketplace_store(self.request.user)
        context["user"] = self.request.user
        return context

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
