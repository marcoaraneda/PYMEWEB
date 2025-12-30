from django.urls import path
from .views import OrderCreateView, OrderDetailView
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

urlpatterns = [
    path('orders/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]



router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = router.urls