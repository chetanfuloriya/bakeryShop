from django.urls import path

from accounts.services import PlaceOrder, Register

urlpatterns = [
    path('register/', Register.as_view(), name='auth_register'),
    path('order_history/', PlaceOrder.as_view(), name='order_history'),
    path('place_order/', PlaceOrder.as_view(), name='place_order'),
]
