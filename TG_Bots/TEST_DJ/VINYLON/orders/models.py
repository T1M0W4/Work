from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from catalogue.models import VinylRecord

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("Пользователь"),
        help_text=_("Пользователь, оформивший заказ.")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания"),
        help_text=_("Дата и время создания заказа.")
    )

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Заказ"),
        help_text=_("Заказ, к которому относится этот элемент.")
    )
    vinyl_record = models.ForeignKey(
        VinylRecord,
        on_delete=models.CASCADE,
        verbose_name=_("Виниловая пластинка"),
        help_text=_("Пластинка, которую пользователь заказал.")
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Количество"),
        help_text=_("Количество заказанных пластинок.")
    )

    class Meta:
        verbose_name = _("Элемент заказа")
        verbose_name_plural = _("Элементы заказа")

    def __str__(self):
        return f"{self.vinyl_record.title} (x{self.quantity})"
