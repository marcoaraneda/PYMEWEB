from rest_framework import generics
from rest_framework.permissions import AllowAny
from apps.stores.models import Store
from apps.stores.serializers import StoreSerializer

class StoreDetailView(generics.RetrieveAPIView):
    queryset = Store.objects.filter(is_active=True)
    lookup_field = 'slug'
    serializer_class = StoreSerializer
    permission_classes = [AllowAny] # Acceso público para el frontend