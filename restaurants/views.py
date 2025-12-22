from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Restaurants, Menu
from .serializers import RestaurantsSerializers, MenuSerializers


@extend_schema(tags=["restaurants"])
class RestaurantListCreateView(GenericAPIView):
    """
    List and create restaurants owned by the authenticated user.

    - GET returns all restaurants where owner == request.user.
    - POST creates a new restaurant and assigns owner=request.user.

    Methods:
        get(request): Return list of restaurants for the user.
        post(request): Create a new restaurant for the user.
    """

    serializer_class = RestaurantsSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = Restaurants.objects.all()

    def get_queryset(self):
        return Restaurants.objects.filter(owner=self.request.user)

    def get(self, request):
        """
        Retrieve restaurants owned by the authenticated user.

        Args:
            request (rest_framework.request.Request): The incoming request.

        Returns:
            rest_framework.response.Response: JSON response with list of the
            user's restaurants (HTTP 200).
        """
        restaurants = self.queryset
        if not restaurants.exists():
            return Response(
                {
                    "msg": "No restaurants found for this user",
                    "data": [],
                    "status": True,
                },
                status=status.HTTP_200_OK,
            )
        serializer = self.serializer_class(restaurants, many=True)
        return Response(
            {
                "msg": "All your restaurants",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        """
        Create a new restaurant owned by the authenticated user.

        Args:
            request (rest_framework.request.Request): The incoming request.
                Payload should match RestaurantsSerializers fields.

        Returns:
            rest_framework.response.Response: JSON response with created
            restaurant data (HTTP 201).

        Side effects:
            Persists a new Restaurants record with owner=request.user.
        """
        user = request.user
        if not user.role == "owner":
            return Response(
                {
                    "msg": "Only users with owner role can create restaurants",
                    "status": False,
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        restaurants = self.get_queryset()
        if restaurants.exists():
            return Response(
                {
                    "msg": "You have already created a restaurant",
                    "status": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(
            {
                "msg": "Restaurant successfully created",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["restaurants"])
class RestaurantDetailView(GenericAPIView):
    """
    Retrieve, update, or delete a single restaurant owned by the user.

    Methods:
        get_object(): Return the restaurant object or raise 404.
        patch(request, pk): Partially update the restaurant.
        delete(request, pk): Delete the restaurant.
    """

    serializer_class = RestaurantsSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Return a Restaurants instance owned by the authenticated user.

        Reads `self.kwargs['pk']` to identify the restaurant.

        Returns:
            Restaurants: The restaurant instance matching pk and owner.

        Raises:
            Http404 if the restaurant does not exist or is not owned by user.
        """
        return get_object_or_404(
            Restaurants,
            pk=self.kwargs["pk"],
            owner=self.request.user,
        )

    def patch(self, request, pk):
        """
        Partially update a restaurant owned by the authenticated user.

        Args:
            request (rest_framework.request.Request): Incoming request with
                partial fields to update.
            pk (int): Path parameter for the restaurant primary key.

        Returns:
            rest_framework.response.Response: JSON response with updated
            restaurant data (HTTP 200).

        Side effects:
            Updates fields on the Restaurants instance.
        """
        restaurant = self.get_object()
        serializer = self.serializer_class(
            restaurant,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "msg": "Restaurant successfully updated",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        """
        Delete a restaurant owned by the authenticated user.

        Args:
            request (rest_framework.request.Request): Incoming request.
            pk (int): Path parameter for the restaurant primary key.

        Returns:
            rest_framework.response.Response: JSON response with success
            message and HTTP 204 status code.

        Side effects:
            Deletes the Restaurants instance from the database.
        """
        restaurant = self.get_object()
        restaurant.delete()
        return Response(
            {"msg": "Restaurant successfully deleted", "status": True},
            status=status.HTTP_204_NO_CONTENT,
        )


@extend_schema(tags=["menu"])
class MenuCreateView(GenericAPIView):
    """
    Create menu items for a restaurant owned by the authenticated user.

    Methods:
        post(request, restaurant_pk): Create a menu item linked to a
            restaurant owned by request.user.
    """

    serializer_class = MenuSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, restaurant_pk):
        """
        Create a new Menu item for the specified restaurant.

        Args:
            request (rest_framework.request.Request): Incoming request with
                menu fields.
            restaurant_pk (int): Path parameter for the parent restaurant.

        Returns:
            rest_framework.response.Response: JSON response with created
            menu data (HTTP 201).

        Side effects:
            Persists a Menu record linked to the restaurant; raises 404 if
            restaurant not found or not owned by the requester.
        """
        restaurant = get_object_or_404(
            Restaurants,
            pk=restaurant_pk,
            owner=request.user,
        )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(restaurant=restaurant)

        return Response(
            {
                "msg": "Menu successfully created",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["menu"])
class MenuDetailView(GenericAPIView):
    """
    Retrieve, update, or delete a specific Menu item belonging to a
    restaurant owned by the requester.

    Methods:
        get_object(): Return the Menu instance or raise 404.
        patch(request, pk): Partially update the menu item.
        delete(request, pk): Delete the menu item.
    """

    serializer_class = MenuSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Return a Menu instance that belongs to a restaurant owned by user.

        Reads `self.kwargs['pk']` for the menu primary key.

        Returns:
            Menu: The menu instance matching pk and owned by user's restaurant.

        Raises:
            Http404 if not found or not owned by the user's restaurant.
        """
        return get_object_or_404(
            Menu,
            pk=self.kwargs["pk"],
            restaurant__owner=self.request.user,
        )

    def patch(self, request):
        """
        Partially update a Menu item.

        Args:
            request (rest_framework.request.Request): Incoming request with
                fields to update.


        Returns:
            rest_framework.response.Response: JSON response with updated
            menu data (HTTP 200).

        Side effects:
            Updates fields on the Menu instance.
        """
        menu = self.get_object()
        serializer = self.serializer_class(
            menu,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "msg": "Menu successfully updated",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request):
        """
        Delete a Menu item belonging to a restaurant owned by the requester.

        Args:
            request (rest_framework.request.Request): Incoming request.

        Returns:
            rest_framework.response.Response: JSON response with success
            message and HTTP 204 status code.

        Side effects:
            Deletes the Menu instance from the database.
        """
        menu = self.get_object()
        menu.delete()
        return Response(
            {"msg": "Menu successfully deleted", "status": True},
            status=status.HTTP_204_NO_CONTENT,
        )
