from django.urls import path
from .views_product_questions import ProductQuestionPublicListAPIView

urlpatterns = [
    path("product/<slug:product_slug>/questions/", ProductQuestionPublicListAPIView.as_view(),
         name="product-questions-public"),
]
