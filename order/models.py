from django.db import models
from cart.models import Cart
from user.models import CustomerUser


class Order(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    ship_address = models.CharField(max_length=255, default='')
    ship_name = models.CharField(max_length=60, default='')
    note = models.TextField(default='')
    is_completed = models.BooleanField(default=False)
