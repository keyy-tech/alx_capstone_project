from restaurants.models import Restaurants, Menu, MenuItem
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request


class CustomerMenuItemsView(GenericAPIView):
    """
    View to retrieve menu items for a specific restaurant.
    """

    def get(self, request: Request, restaurant_id: int) -> Response:
        # Retrieve the restaurant or return 404 if not found
        restaurant = get_object_or_404(Restaurants, id=restaurant_id)

        # Retrieve the menu associated with the restaurant
        menu = get_object_or_404(Menu, restaurant=restaurant)

        # Retrieve all menu items for the menu
        menu_items = MenuItem.objects.filter(menu=menu)

        # Prepare the response data
        items_data = [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
            }
            for item in menu_items
        ]

        return Response(items_data, status=status.HTTP_200_OK)
