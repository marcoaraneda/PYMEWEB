from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q

from apps.orders.models import Order
from apps.catalogo.models import Product
from apps.stores.models import Store
from apps.usuarios.models import StoreMembership
from apps.resenas.models import Review
from apps.resenas.serializers import ReviewFeedSerializer
from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.select_related("store", "created_by")
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        store_param = self.request.query_params.get("store")

        if user.is_staff:
            if store_param:
                qs = qs.filter(store__slug=store_param)
            return qs

        store_ids = list(
            StoreMembership.objects.filter(user=user, is_active=True).values_list("store_id", flat=True)
        )

        filters = Q(created_by=user) | Q(store_id__in=store_ids)
        qs = qs.filter(filters)

        if store_param:
            qs = qs.filter(store__slug=store_param)

        return qs

    def perform_create(self, serializer):
        # created_by se setea aquí; store ya viene resuelta por SlugRelatedField
        serializer.save(created_by=self.request.user)


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        store_param = request.query_params.get("store")
        user = request.user

        # Limita las tiendas a las que el usuario pertenece (o staff ve todas)
        if user.is_staff:
            base_stores = Store.objects.all()
        else:
            membership_ids = StoreMembership.objects.filter(user=user, is_active=True).values_list("store_id", flat=True)
            base_stores = Store.objects.filter(id__in=membership_ids)

        # Aplica filtro por slug si se envía y coincide con las tiendas accesibles
        if store_param:
            stores_qs = base_stores.filter(slug=store_param)
        else:
            stores_qs = base_stores

        active_stores = stores_qs.filter(is_active=True).count()

        orders_qs = Order.objects.filter(store__in=stores_qs)
        now = timezone.now()
        visits_last_7d = orders_qs.filter(created_at__gte=now - timedelta(days=7)).count()
        conversions = orders_qs.filter(status__in=["completed", "delivered"]).count()
        pending_orders = orders_qs.filter(status__in=["pending", "preparing", "in_transit"]).count()
        new_orders_24h = orders_qs.filter(created_at__gte=now - timedelta(hours=24)).count()

        tickets_qs = Ticket.objects.filter(store__in=stores_qs)
        support_open = tickets_qs.filter(status__in=[Ticket.STATUS_OPEN, Ticket.STATUS_IN_PROGRESS]).count()
        tickets_updated_24h = tickets_qs.filter(updated_at__gte=now - timedelta(hours=24)).count()
        latest_tickets = list(
            tickets_qs.order_by("-updated_at").values("id", "title", "status", "priority", "updated_at", "store__slug")[:3]
        )

        pending_products = Product.objects.filter(store__in=stores_qs, is_active=False).count()

        notifications = []
        if support_open:
            notifications.append({"type": "ticket", "message": f"{support_open} tickets abiertos", "count": support_open})
        if tickets_updated_24h:
            notifications.append({"type": "ticket_update", "message": f"{tickets_updated_24h} tickets actualizados (24h)", "count": tickets_updated_24h})
        for t in latest_tickets:
            notifications.append(
                {
                    "type": "ticket_detail",
                    "message": f"Ticket: {t['title']} ({t['status']})",
                    "count": 1,
                    "store": t.get("store__slug"),
                    "ticket_id": t.get("id"),
                    "status": t.get("status"),
                }
            )
        if pending_orders:
            notifications.append({"type": "order", "message": f"{pending_orders} pedidos pendientes/en curso", "count": pending_orders})
        if new_orders_24h:
            notifications.append({"type": "order_new", "message": f"{new_orders_24h} pedidos nuevos (24h)", "count": new_orders_24h})
        if pending_products:
            notifications.append({"type": "product", "message": f"{pending_products} productos pendientes", "count": pending_products})

        data = {
            "active_stores": active_stores,
            "visits_last_7d": visits_last_7d,
            "conversions": conversions,
            "support_open": support_open,
            "pending_products": pending_products,
            "pending_orders": pending_orders,
            "new_orders_24h": new_orders_24h,
            "tickets_updated_24h": tickets_updated_24h,
            "notifications": notifications,
        }
        return Response(data)


class RecentReviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        store_param = request.query_params.get("store")
        limit_param = request.query_params.get("limit")
        try:
            limit = max(1, int(limit_param)) if limit_param else 8
        except (TypeError, ValueError):
            limit = 8

        user = request.user
        if user.is_staff:
            stores_qs = Store.objects.all()
        else:
            membership_ids = StoreMembership.objects.filter(user=user, is_active=True).values_list("store_id", flat=True)
            stores_qs = Store.objects.filter(id__in=membership_ids)

        if store_param:
            stores_qs = stores_qs.filter(slug=store_param)

        if not stores_qs.exists():
            return Response([])

        reviews_qs = (
            Review.objects.filter(store__in=stores_qs)
            .exclude(status=Review.REJECTED)
            .select_related("product", "store")
            .order_by("-created_at")
        )

        data = ReviewFeedSerializer(reviews_qs[:limit], many=True).data
        return Response(data)
