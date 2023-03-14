import json

from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from books.models import Book
from cart.models import Cart, CartItem
from user.models import CustomerUser
from order.models import Order
from django.contrib.auth import authenticate, login, decorators, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib import messages

class HomeView(View):
    def get(self, request):
        context = pagination(request)

        return render(request, 'homepage/index.html', context)


class ItemView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        customer = request.user
        if str(customer) != 'AnonymousUser':
            cart, created = Cart.objects.get_or_create(user=customer)
            cart_items = cart.cartitem_set.all()
            quantity = cart.get_cart_quantity
            context = {"data": book, "user": customer, "cart_items": cart_items, "quantity": quantity, "cart": cart}
        else:
            cart_items = []
            cart = []
            context = {"data": book, "user": customer, "cart_items": cart_items, "quantity": 0, "cart": cart}

        return render(request, 'item/index.html', context)


class LoginClass(View):
    def get(self, request):
        return render(request, 'login/login.html', {})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        myUser = authenticate(username=username, password=password)

        if myUser is None:
            messages.add_message(request, messages.ERROR, 'Hello world')
            return render(request, 'login/login.html')
        login(request, myUser)

        return redirect(request.GET['next'])


class CartView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        customer = request.user
        cart, created = Cart.objects.get_or_create(user=customer)
        cart_items = cart.cartitem_set.all()
        quantity = cart.get_cart_quantity

        context = {"cart_items": cart_items, "cart": cart, "quantity": quantity, "user": customer}
        return render(request, 'cart/index.html', context)


class SignUp(View):
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        for item in CustomerUser.objects.all():
            if item.username == username:
                messages.add_message(request, messages.INFO, "Sign up failed")
                return redirect('/login?next=/')

        user = CustomerUser(username=username, email=email, phone_number=phone_number)
        user.set_password(password)
        user.save()
        messages.add_message(request, messages.SUCCESS, "Sign up Success")
        return redirect('/login?next=/')


@decorators.login_required(login_url='/login/')
def checkOutView(request):
    customer = request.user
    cart, created = Cart.objects.get_or_create(user=customer)
    cart_items = cart.cartitem_set.all()
    quantity = cart.get_cart_quantity
    context = {"cart": cart, "cart_items": cart_items, "quantity": quantity}
    return render(request, 'cart/checkout.html', context)


# POST Cart method
@csrf_exempt
def updateCart(request):
    data = json.loads(request.body)
    id = data['id']
    action = data['action']
    template = data['template']

    print(id)

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

    books_list = Book.objects.all()
    total_items = 4
    p = Paginator(books_list, total_items)
    page = request.GET.get('page', 1)
    # print(page)
    books = p.get_page(page)

    if str(customer) != 'AnonymousUser':
        cart, created = Cart.objects.get_or_create(user=customer)
        cart_items = cart.cartitem_set.all()
        quantity = cart.get_cart_quantity
        context = {"data": books, "user": customer, "cart_items": cart_items, "quantity": quantity, "cart": cart}
    else:
        cart_items = []
        cart = []
        context = {"data": books, "user": customer, "quantity": 0, "cart_items": cart_items, "cart": cart}

    if template == 'homepage':
        html = render_to_string('homepage/navbar.html', context)
        return JsonResponse(html, safe=False)

    elif template == 'cart':
        html = render_to_string('cart/cart-content.html', context)
        return JsonResponse(html, safe=False)


def userLogOut(request):
    logout(request)
    return HttpResponseRedirect('/')


# POST Order method
@csrf_exempt
def saveOrder(request):
    data = json.loads(request.body)
    print(data)

    customer = request.user
    cart, created = Cart.objects.get_or_create(user=customer)
    order, created = Order.objects.get_or_create(user=customer, cart=cart)
    order.ship_name = data['name']
    order.ship_address = data['address']
    order.note = data['note']

    order.save()

    return JsonResponse('Order is success', safe=False)


def paginationItems(request):
    context = pagination(request)

    html = render_to_string('homepage/page-content.html', context)

    return JsonResponse(html, safe=False)


def pagination(request):
    query = request.GET.get('q', '')

    if query == '':
        books_list = Book.objects.all()
        print(books_list)
    else:
        books_list = Book.objects.filter(title__icontains=query)
        print(books_list)

    total_items = 3
    p = Paginator(books_list, total_items)
    page = request.GET.get('page', 1)
    books = p.get_page(page)
    print(books)

    customer = request.user
    if str(customer) != 'AnonymousUser':
        cart, created = Cart.objects.get_or_create(user=customer)
        cart_items = cart.cartitem_set.all()
        quantity = cart.get_cart_quantity
        context = {"data": books, "user": customer, "cart_items": cart_items, "quantity": quantity, "cart": cart, "q": query}
    else:
        cart_items = []
        cart = []
        context = {"data": books, "user": customer, "quantity": 0, "cart_items": cart_items, "cart": cart, "q": query}

    return context
