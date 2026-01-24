from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TicketViewSet, DashboardSummaryView

router = DefaultRouter()
router.register(r"tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("dashboard/summary/", DashboardSummaryView.as_view(), name="dashboard-summary"),
    path("", include(router.urls)),
]
