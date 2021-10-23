# django
from django.urls import path

# local
from . import views

app_name = "payments_app"

urlpatterns = [
    # donar con mercadopago
    path(
        'api/payments/donations/mercadopago/',
        views.mercadopago.as_view(),
    ),
]
