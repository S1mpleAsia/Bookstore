from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('item/<int:id>', ItemView.as_view(), name='item'),
    path('cart/', CartView.as_view(), name='cart'),
    path('login/', LoginClass.as_view(), name='login'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('update-cart/', updateCart, name='update-cart'),
    path('checkout/', checkOutView, name='checkout'),
    path('save-order/', saveOrder, name='save-order'),
    path('get/pagination/', paginationItems, name='pagination'),
]