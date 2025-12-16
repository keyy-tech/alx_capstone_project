from django.db import models

from restaurants.models import Menu
from users.models import User


# Create your models here.


class Order(models.Model):
    ORDERCHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=ORDERCHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.email}"

    class Meta:
        ordering = ["-order_date"]


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    menu_item = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} of {self.menu_item.name} in Order {self.order.id}"
