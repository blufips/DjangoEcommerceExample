from django.urls import path
from .views import StoreView, CartView, CheckoutView, updateItem, processOrder


urlpatterns = [
    path('', StoreView.as_view(), name='store'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('update_item/', updateItem, name='update_item'),
    path('process_order/', processOrder, name='process_order'),
]
