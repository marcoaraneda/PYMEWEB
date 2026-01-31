from django.urls import path
from .views_owner import OwnerReviewsListAPIView

urlpatterns = [
    path("reviews/", OwnerReviewsListAPIView.as_view(), name="owner-reviews"),
]
