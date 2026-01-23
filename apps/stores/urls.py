from django.urls import path
from .views import StoreListCreateView, StoreDetailView, MyStoresView

urlpatterns = [
    path("", StoreListCreateView.as_view(), name="store-list"),          # 👈 /api/stores/
    path("mine/", MyStoresView.as_view(), name="store-mine"),
    path("<slug:slug>/", StoreDetailView.as_view(), name="store-detail"),
]
