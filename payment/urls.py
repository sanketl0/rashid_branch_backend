from .views import *
from django.urls import include, path

urlpatterns = [
    path('pay/', start_payment.as_view(), name="payment"),
    path('success/', handle_payment_success.as_view(), name="payment_success")
]