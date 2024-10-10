from django.urls import path
from .views import OrderListView, OrderDetailView, CreateOrderView

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('create/', CreateOrderView.as_view(), name='order_create'),
]