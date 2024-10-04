from django.db import models
from django.contrib.auth.models import User
from django.db import models
from vinyls.models import VinylRecord

class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vinyl_records = models.ManyToManyField(VinylRecord)

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vinyl_records = models.ManyToManyField(VinylRecord)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"
