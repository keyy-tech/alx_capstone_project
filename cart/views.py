from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


@extend_schema(tags=["cart"])
class CartView(GenericAPIView):
    """
    Retrieve and manage the authenticated user's cart.

    This view provides endpoints to fetch the current user's cart and to
    clear all items from it. If a cart does not exist for the authenticated
    user, `get_object` will create one.

    Methods:
        get_object(): Return or create a Cart for `request.user`.
        get(request): Return serialized cart data.
        delete(request): Remove all items from the cart (clears cart).
    """

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Return the Cart for the authenticated user, creating it if missing.

        Args:
            self: view instance (uses self.request.user).

        Returns:
            cart (Cart): The Cart instance for the current user.

        Side effects:
            May create a new Cart in the database.
        """
        cart, _ = Cart.objects.get_or_create(customer=self.request.user)
        return cart

    def get(self, request):
        """
        Retrieve the authenticated user's cart.

        Args:
            request (rest_framework.request.Request): The incoming request.

        Returns:
            rest_framework.response.Response: JSON response containing the
            serialized cart data and a success message (HTTP 200).
        """
        cart = self.get_object()
        serializer = self.serializer_class(cart)
        return Response(
            {
                "msg": "User cart retrieved successfully",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request):
        """
        Clear all items from the authenticated user's cart.

        Args:
            request (rest_framework.request.Request): The incoming request.

        Returns:
            rest_framework.response.Response: JSON response with a success
            message (HTTP 200).

        Side effects:
            Deletes all CartItem records associated with the user's Cart.
        """
        cart = self.get_object()
        cart.items.all().delete()
        return Response(
            {
                "msg": "Cart cleared successfully",
                "status": True,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["cart-items"])
class CartItemCreateView(GenericAPIView):
    """
    Add an item to the authenticated user's cart or update its quantity.

    Expects request.data to contain at least a `menu` field (menu id) and
    optional `quantity` (defaults to 1). If the cart item already exists,
    its quantity is incremented by the requested amount; otherwise a new
    CartItem is created.

    Methods:
        post(request): Validate input and create/update a CartItem.
    """

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Create or update a CartItem for the authenticated user's cart.

        Args:
            request (rest_framework.request.Request): The incoming request.
                Expected payload: {"menu": <int>, "quantity": <int, optional>}.

        Returns:
            rest_framework.response.Response: JSON response containing the
            serialized CartItem and a success message (HTTP 201).

        Side effects:
            Creates the user's Cart if it does not exist. Creates or updates
            a CartItem and saves it to the database.
        """
        cart, created = Cart.objects.get_or_create(customer=request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        menu = serializer.validated_data["menu"]
        quantity = serializer.validated_data.get("quantity", 1)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, menu=menu, quantity=quantity
        )

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        serializer = self.serializer_class(cart_item)
        data = {
            "msg": "Item added to cart successfully",
            "data": serializer.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["cart-items"])
class CartItemDeleteView(GenericAPIView):
    """
    Remove or update an individual cart item belonging to the authenticated user.

    Provides delete to remove an item and patch to update its quantity.

    Methods:
        delete(request, item_id): Remove the specified CartItem.
        patch(request, item_id): Update the quantity for the specified CartItem.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def delete(self, request, item_id):
        """
        Remove a CartItem from the authenticated user's cart.

        Args:
            request (rest_framework.request.Request): The incoming request.
            item_id (int): The id of the CartItem to delete (path parameter).

        Returns:
            rest_framework.response.Response: JSON response with a success
            message (HTTP 200).

        Side effects:
            Deletes the CartItem from the database.
        """
        cart = get_object_or_404(Cart, customer=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        return Response(
            {
                "msg": "Item removed from cart successfully",
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, item_id):
        """
        Update the quantity of a CartItem in the authenticated user's cart.

        Args:
            request (rest_framework.request.Request): The incoming request.
                Expected payload: {"quantity": <int>}.
            item_id (int): The id of the CartItem to update (path parameter).

        Returns:
            rest_framework.response.Response: JSON response containing the
            updated serialized CartItem and a success message (HTTP 200), or
            an error response (HTTP 400) for invalid quantity input.

        Side effects:
            Modifies the CartItem.quantity and saves the object.
        """
        cart = get_object_or_404(Cart, customer=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        quantity = request.data.get("quantity")
        if not quantity or int(quantity) < 0:
            return Response(
                {
                    "msg": "Invalid quantity",
                    "status": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        cart_item.quantity = int(quantity)
        cart_item.save()
        serializer = self.serializer_class(cart_item)
        data = {
            "msg": "Item quantity updated successfully",
            "data": serializer.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)
