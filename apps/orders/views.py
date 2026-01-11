from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Order
from .serializers import OrderSerializer, OrderDetailSerializer


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
