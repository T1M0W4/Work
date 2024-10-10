from django.views.generic import ListView, DetailView, CreateView
from .models import Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy("orders:order_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

