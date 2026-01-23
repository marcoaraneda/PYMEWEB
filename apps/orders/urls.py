from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import OrderViewSet, TopProductsView

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='orders')

urlpatterns = [
	path('store/<slug:store_slug>/top-products/', TopProductsView.as_view(), name='top-products'),
]
urlpatterns += router.urls
