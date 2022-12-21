import json

from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from books.models import Book
from cart.models import Cart, CartItem
from user.models import CustomerUser
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class HomeView(View):
    def get(self, request):
        books = Book.objects.all()
        customer = request.user
        if str(customer) != 'AnonymousUser':
            cart, created = Cart.objects.get_or_create(user=customer)
            cart_items = cart.cartitem_set.all()
            quantity = cart.get_cart_quantity
            context = {"data": books, "user": customer, "cart_items": cart_items, "quantity": quantity, "cart": cart}
        else:
            cart_items = []
            cart = []
            context = {"data": books, "user": customer, "quantity": 0, "cart_items": cart_items, "cart": cart}
        return render(request, 'homepage/index.html', context)


class ItemView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        customer = request.user
        cart, created = Cart.objects.get_or_create(user=customer)
        quantity = cart.get_cart_quantity
        context = {"data": book, "quantity": quantity}
        return render(request, 'item/index.html', context)


class LoginClass(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login/login.html', {})
        else:
            return redirect('/cart/')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        myUser = authenticate(username=username, password=password)

        if myUser is None:
            return HttpResponse('User khong ton tai')
        login(request, myUser)
        return redirect('/cart/')


class CartView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')

        customer = request.user
        cart, created = Cart.objects.get_or_create(user=customer)
        cart_items = cart.cartitem_set.all()
        quantity = cart.get_cart_quantity

        context = {"cart_items": cart_items, "cart": cart, "quantity": quantity}
        return render(request, 'cart/index.html', context)


class SignUp(View):
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        for item in CustomerUser.objects.all():
            if item.username == username:
                return HttpResponse("Them moi that bai")

        user = CustomerUser(username=username, email=email, phone_number=phone_number)
        user.set_password(password)
        user.save()
        return HttpResponse("Them moi thanh cong")


class CheckOut(View):
    def get(self, request):
        return render(request, 'cart/checkout.html', {})


@csrf_exempt
def updateCart(request):
    data = json.loads(request.body)
    id = data['id']
    action = data['action']

    customer = request.user
    book = Book.objects.get(id=id)
    cart, created = Cart.objects.get_or_create(user=customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=book)

    if action == 'add':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'remove':
        cart_item.quantity -= 1
        cart_item.save()
    elif action == 'delete':
        cart_item.delete()

    if cart_item.quantity <= 0:
        cart_item.delete()

    return JsonResponse('Item was added', safe=False)
