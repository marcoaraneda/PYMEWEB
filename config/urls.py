"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.stores.views import StoreDetailView
from apps.catalogo.views_public import MarketplaceProductListAPIView
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    # ================= ADMIN =================
    path("admin/", admin.site.urls),

    # ================= API =================
    path("api/stores/", include("apps.stores.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/users/", include("apps.usuarios.urls")),
    path("api/support/", include("apps.support.urls")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/marketplace/products/", MarketplaceProductListAPIView.as_view(), name="marketplace-products"),

    # ============ API POR TIENDA ============
    path("api/store/<slug:store_slug>/catalogo/", include("apps.catalogo.urls")),
    path("api/store/<slug:store_slug>/catalogo/", include("apps.catalogo.urls_public")),
    path("api/store/<slug:store_slug>/cms/", include("apps.cms.urls")),
    path("api/store/<slug:store_slug>/cms/", include("apps.cms.urls_public")),

    path("api/store/<slug:store_slug>/admin/catalogo/", include("apps.catalogo.urls_admin")),
    path("api/store/<slug:store_slug>/admin/inventario/", include("apps.inventario.urls_admin")),
    path("api/store/<slug:store_slug>/admin/cms/", include("apps.cms.urls_admin")),

    path("api/store/<slug:store_slug>/resenas/", include("apps.resenas.urls")),
    path("api/store/<slug:store_slug>/admin/resenas/", include("apps.resenas.urls_admin")),

    path("api/store/<slug:store_slug>/faq/", include("apps.faq.urls")),
    path("api/store/<slug:store_slug>/faq/", include("apps.faq.urls_product_questions")),
    path("api/store/<slug:store_slug>/admin/faq/", include("apps.faq.urls_admin")),
    path('api/payments/', include('apps.payments.urls')),
    

    # ================= FRONT (SIEMPRE AL FINAL) =================
    path("<slug:slug>/", StoreDetailView.as_view(), name="store-detail"),

    ]+ static(settings.MEDIA_URL,               document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )