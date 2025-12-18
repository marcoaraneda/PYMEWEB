from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_admin import FAQItemAdminViewSet, ProductQuestionAdminViewSet

router = DefaultRouter()
router.register(r"faqs", FAQItemAdminViewSet, basename="admin-faqs")
router.register(r"product-questions", ProductQuestionAdminViewSet, basename="admin-product-questions")

urlpatterns = [
    path("", include(router.urls)),
]
