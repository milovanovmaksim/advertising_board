from django.db import models
from django.conf import settings

from main.models import Category

CustomUser = settings.AUTH_USER_MODEL


class Subscription(models.Model):
    users = models.ManyToManyField(CustomUser, related_name='subscription', verbose_name='Пользователи')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='subscription', verbose_name='Категория объявления')

    class Meta:
        verbose_name = "Подписка/Подписку"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f'Категория объявления: {self.category.title}'
