from django.urls import path
from .views import FAQItemPublicListAPIView

urlpatterns = [
    path("faqs/", FAQItemPublicListAPIView.as_view(), name="faqs-public"),
]
