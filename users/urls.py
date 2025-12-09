from django.urls import path
from . import views

urlpatterns = [
    path(
        "register/customer/",
        views.RegisterCustomerView.as_view(),
        name="register_customer",
    ),
    path("register/owner/", views.RegisterOwnerView.as_view(), name="register_owner"),
]
