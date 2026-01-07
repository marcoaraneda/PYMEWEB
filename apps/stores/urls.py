from django.urls import path
from .views import StoreListView, StoreDetailView

urlpatterns = [
    path("", StoreListView.as_view(), name="store-list"),          # 👈 /api/stores/
    path("<slug:slug>/", StoreDetailView.as_view(), name="store-detail"),
]
