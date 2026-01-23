from django.urls import path
from .views import ReviewPublicListAPIView, ReviewCreateAPIView

urlpatterns = [
    path("reviews/", ReviewPublicListAPIView.as_view(), name="reviews-public"),
    path("reviews/product/<slug:product_slug>/", ReviewPublicListAPIView.as_view(), name="reviews-public-by-product"),
    path("reviews/product/<slug:product_slug>/create/", ReviewCreateAPIView.as_view(), name="reviews-create"),
]
