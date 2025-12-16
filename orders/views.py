from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart


@extend_schema(tags=["orders"], request=None)
class OrderCreateView(GenericAPIView):
    """
    Place an order for the authenticated user using their cart contents.

    This view converts the user's Cart and CartItems into an Order and
    related OrderItem records, computes totals, and deletes the cart after
    successfully placing the order.

    Methods:
        post(request): Create an Order from the authenticated user's Cart.
    """

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Create an Order from the authenticated user's Cart.

        Args:
            request (rest_framework.request.Request): Incoming request from
                an authenticated user.

        Returns:
            rest_framework.response.Response: JSON response containing the
            created order data and HTTP 201 on success, or an error response
            (HTTP 400) if the cart is empty.

        Side effects:
            Reads the Cart, creates Order and OrderItem records, and deletes
            the Cart after successful order creation.
        """
        if not Cart.objects.filter(user=self.request.user).exists():
            return Response(
                {
                    "msg": "Cart is empty. Cannot place order.",
                    "status": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = Cart.objects.prefetch_related("items").get(user=request.user)
        cart.calculate_total_price()

        order = Order.objects.create(
            customer=request.user,
            status="PENDING",
            total_amount=cart.total_price,
        )

        order_item_to_create = []

        for item in cart.items.all():
            order_item_to_create.append(
                OrderItem(
                    order=order,
                    menu_item=item.menu_item,
                    quantity=item.quantity,
                    price=item.cart_item_price(),
                )
            )

        OrderItem.objects.bulk_create(order_item_to_create)

        cart.delete()
        serializer = self.serializer_class(order)
        return Response(
            {
                "msg": "Order placed successfully",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_201_CREATED,
        )
