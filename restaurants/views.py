from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Restaurants, Menu
from .serializers import RestaurantsSerializers, MenuSerializers


@extend_schema(tags=["restaurants"])
class RestaurantListCreateView(GenericAPIView):
    serializer_class = RestaurantsSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Restaurants.objects.filter(owner=self.request.user)

    def get(self, request):
        restaurants = self.get_queryset()
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
    serializer_class = RestaurantsSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Restaurants,
            pk=self.kwargs["pk"],
            owner=self.request.user,
        )

    def patch(self, request, pk):
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
        restaurant = self.get_object()
        restaurant.delete()
        return Response(
            {"msg": "Restaurant successfully deleted", "status": True},
            status=status.HTTP_204_NO_CONTENT,
        )


@extend_schema(tags=["menu"])
class MenuCreateView(GenericAPIView):
    serializer_class = MenuSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, restaurant_pk):
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
    serializer_class = MenuSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Menu,
            pk=self.kwargs["pk"],
            restaurant__owner=self.request.user,
        )

    def patch(self, request, pk):
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

    def delete(self, request, pk):
        menu = self.get_object()
        menu.delete()
        return Response(
            {"msg": "Menu successfully deleted", "status": True},
            status=status.HTTP_204_NO_CONTENT,
        )
