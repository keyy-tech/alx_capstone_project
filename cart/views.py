from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


@extend_schema(tags=["cart"])
class CartView(GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(customer=self.request.user)
        return cart

    def get(self, request):
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
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
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
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def delete(self, request, item_id):
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
