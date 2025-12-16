from django.urls import path
from .views import (
    RestaurantListCreateView,
    RestaurantDetailView,
    MenuCreateView,
    MenuDetailView,
)

urlpatterns = [
    # Restaurants
    path("restaurants/", RestaurantListCreateView.as_view(), name="restaurant-list"),
    path(
        "restaurants/<int:pk>/",
        RestaurantDetailView.as_view(),
        name="restaurant-detail",
    ),
    # Menus
    path(
        "restaurants/<int:restaurant_pk>/menu/",
        MenuCreateView.as_view(),
        name="menu-create",
    ),
    path(
        "menu/<int:pk>/",
        MenuDetailView.as_view(),
        name="menu-detail",
    ),
]
