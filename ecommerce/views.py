from django.shortcuts import render
from .models import Cart, CartItem, Event, Order, OrderItem


def add_product_in_cart(request, pk):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Event.objects.get(pk=pk)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()


def confirm_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    order = Order.objects.create(user=request.user)

    for cart_item in cart_items:
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

        cart_item.delete()

