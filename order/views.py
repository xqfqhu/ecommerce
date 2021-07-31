from django.shortcuts import render
from .models import Order, OrderItem
# Create your views here.


def user_orders(request):
    user = request.user
    order = Order.objects.filter(user=user).filter(
        billing_status=True).prefetch_related("items")
    return order
