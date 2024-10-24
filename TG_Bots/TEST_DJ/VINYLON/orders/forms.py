# forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  # Убираем поле user
        labels = {}

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["vinyl_record", "quantity"]
        labels = {
            "vinyl_record": _("Виниловая пластинка"),
            "quantity": _("Количество"),
        }
