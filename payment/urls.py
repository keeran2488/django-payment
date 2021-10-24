from django.urls import path

from payment.views import *

app_name = "payment"

urlpatterns=[
    path("khalti/verify/", KhaltiVerifyPayment.as_view(), name="khalti_verify"),
    path("home/", home, name="home"),
    path("success/", success, name="success"),
    path("fail/", fail, name="fail"),
    path("esewa/", esewa, name="esewa"),
    path("esewa/verify/", EsewaVerifyView.as_view(), name="esewa_verify"),
]