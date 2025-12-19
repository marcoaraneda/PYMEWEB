from django.urls import path
from apps.stores.views import StoreDetailView

urlpatterns = [
    path('<slug:slug>/', StoreDetailView.as_view(), name='store-detail'),
]