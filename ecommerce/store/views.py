from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    TemplateView,
    ListView
    )
from .models import (
    Customer,
    Product,
    Order,
    OrderItem,
    ShippingAddress,
)
from .utils import cookie_cart, cart_data, guest_order
from django.http import JsonResponse
import json
import datetime

class StoreView(ListView):
    model = Product
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cart_data(self.request)
        cart_items = data['cart_items']
        context['cart_items'] = cart_items
        return context


class CartView(TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cart_data(self.request)
        cart_items = data['cart_items']
        order = data['order']
        items = data['items']
        context['items'] = items
        context['order'] = order
        context['cart_items'] = cart_items
        return context


class CheckoutView(TemplateView):
    template_name = 'store/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cart_data(self.request)
        cart_items = data['cart_items']
        order = data['order']
        items = data['items']
        context['items'] = items
        context['order'] = order
        context['cart_items'] = cart_items
        return context


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(f"productId: {productId}\nAction: {action}")
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guest_order(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
    return JsonResponse('Payment submitted..', safe=False)
