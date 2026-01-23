from django.urls import path
from .views import init_webpay, webpay_return

urlpatterns = [
    path('webpay/init/', init_webpay, name='init_webpay'),
    path('webpay/return/', webpay_return, name='webpay_return'),
]
