from django.db import models

from restaurants.models import Menu
from users.models import User


# Create your models here.
class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.username

    def calculate_total_price(self):
        total = sum(item.cart_item_price() for item in self.items.all())
        self.total_price = total
        self.save()
        return self.total_price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    def cart_item_price(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.menu_item.name} in {self.cart.customer.username}'s cart"
