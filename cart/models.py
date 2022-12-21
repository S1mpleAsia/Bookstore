from django.db import models
from books.models import Book
from user.models import CustomerUser


class Cart(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    @property
    def get_cart_total(self):
        cart_items = self.cartitem_set.all()
        total = 0
        for item in cart_items:
            total += item.get_total

        return total

    @property
    def get_cart_quantity(self):
        cart_item = self.cartitem_set.all()
        total_quantity = 0
        for item in cart_item:
            total_quantity += item.quantity

        return total_quantity


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total
