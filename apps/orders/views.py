from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderDetailSerializer
from apps.catalogo.serializers import ProductSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')

    permission_classes_by_action = {
        'create': [AllowAny],
        'retrieve': [AllowAny],   # 👈 SUCCESS PÚBLICO
        'list': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
        'destroy': [IsAuthenticated],
    }

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_classes_by_action.get(
                self.action,
                self.permission_classes
            )
        ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        store_param = self.request.query_params.get('store')
        if store_param:
            qs = qs.filter(store__slug=store_param)
        return qs

    @action(detail=False, methods=['get'], url_path='pending')
    def pending(self, request):
        store_param = request.query_params.get('store')
        qs = self.get_queryset().filter(status__in=['pending', 'preparing']).order_by('-created_at')
        if store_param:
            qs = qs.filter(store__slug=store_param)
        serializer = OrderSerializer(qs[:10], many=True)
        return Response(serializer.data)


class TopProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, store_slug: str):
        limit = int(request.query_params.get("limit", 5))
        qs = (
            OrderItem.objects.filter(order__store__slug=store_slug)
            .values("product")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")[:limit]
        )
        product_ids = [row["product"] for row in qs]
        products = {p.id: p for p in OrderItem._meta.get_field("product").related_model.objects.filter(id__in=product_ids)}
        data = []
        for row in qs:
            product = products.get(row["product"])
            if product:
                serialized = ProductSerializer(product).data
                serialized["total_quantity"] = row["total_quantity"]
                data.append(serialized)
        return Response(data)
