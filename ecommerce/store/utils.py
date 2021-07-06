import json
from .models import (
    Customer,
    Product,
    Order,
    OrderItem,
    ShippingAddress,
)


def cookie_cart(request):
    # TRY TO GET THE COOKIE CART
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart: ', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_items']
    # LOOP TO THE EVERY ITEM IN COOKIE CART USING ID AS KEY
    for i in cart:
        try:
            # UPDATE THE CART INDIVIDUAL ITEM
            cart_items += cart[i]['quantity']
            # GET THE PRODUCT USING ID
            product = Product.objects.get(id=i)
            # GET THE TOTAL PRICE
            total = product.price * cart[i]['quantity']
            # UPDATE THE TOTAL PRICE
            order['get_cart_total'] += total
            # UPDATE THE TOTAL NUMBER OF CART ITEMS
            order['get_cart_items'] += cart[i]['quantity']
            # SET THE ITEM INFORMATION
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            # UPDATE THE ITEMS
            items.append(item)
            # CHECK THE PRODUCT IF NEED TO SHIPPING
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cart_items': cart_items, 'order': order, 'items': items}

def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # Find else Create an Order object
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # Get the all order items
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        cart_items = cookie_data['cart_items']
        order = cookie_data['order']
        items = cookie_data['items']
    return {'cart_items': cart_items, 'order': order, 'items': items}

def guest_order(request, data):
    print("User is not login...")
    print('COOKIES', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    data = cookie_cart(request)
    items = data['items']
    # GET OR CREATE A CUSTOMER USING THE EMAIL
    customer, created = Customer.objects.get_or_create(email=email)
    # SET THE CUSTOMER NAME
    customer.name = name
    customer.save()
    order = Order.objects.create(customer=customer, complete=False)
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])
    return customer, order
