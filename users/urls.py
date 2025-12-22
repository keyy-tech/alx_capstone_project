from django.urls import path
from . import views

urlpatterns = [
    path(
        "register/",
        views.RegisterCustomerView.as_view(),
        name="register_customer",
    ),
    path(
        "update_role/<str:user_id>/",
        views.AdminUpdateRoleView.as_view(),
        name="update_user_role",
    ),
]
