from django.urls import path
from .views import CartView, CartItemCreateView, CartItemDeleteView


urlpatterns = [
    path("cart/", CartView.as_view(), name="cart-detail"),
    path("cart/items/", CartItemCreateView.as_view(), name="cart-item-create"),
    path(
        "cart/items/<int:pk>/",
        CartItemDeleteView.as_view(),
        name="cart-item-delete",
    ),
]
