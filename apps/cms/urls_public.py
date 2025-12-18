from django.urls import path
from .views_public import HomeSectionsPublicAPIView, PagePublicRetrieveAPIView

urlpatterns = [
    path("home/", HomeSectionsPublicAPIView.as_view(), name="cms-home-public"),
    path("pages/<str:page_type>/", PagePublicRetrieveAPIView.as_view(), name="cms-page-public"),
]
