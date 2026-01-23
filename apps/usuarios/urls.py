from django.urls import path
from .views import MeView, PasswordChangeView, SignupView

urlpatterns = [
    path("me/", MeView.as_view(), name="user-me"),
    path("change-password/", PasswordChangeView.as_view(), name="user-change-password"),
    path("signup/", SignupView.as_view(), name="user-signup"),
]
