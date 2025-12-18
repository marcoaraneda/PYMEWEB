from django.urls import path, include

urlpatterns = [
    path("", include("apps.cms.urls_public")),
    path("admin/", include("apps.cms.urls_admin")),  # si existe
]
