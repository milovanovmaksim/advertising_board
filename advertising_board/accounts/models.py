from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):

    def get_user_by_email(self, email):
        user = None
        try:
            user = self.get(email=email)
        except CustomUser.DoesNotExist:
            pass
        return user


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    def is_common(self):
        return self.groups.filter(name='common_users').exists()

    def is_banned(self):
        return self.groups.filter(name='banned_users').exists()


class CustomSellerManager(models.Manager):
    def update_seller(self, user_form, seller_form):
        user = user_form.save()
        seller = seller_form.save(commit=False)
        seller.user = user
        seller.save()
        return seller


class Seller(models.Model):
    seller = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    itn = models.CharField(max_length=100, verbose_name='ИНН', blank=True)
    img = models.ImageField(upload_to='profile/', default='profile/default_user_logo.png')
    phone_number = models.CharField(max_length=12, verbose_name="Номер телефона", blank=True)

    objects = CustomSellerManager()

    class Meta:
        verbose_name = 'Продавца'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return f'{self.seller}'

    @property
    def number_ads(self):
        return self.ads.count()


class SMSLog(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False, verbose_name='Подтвержден')
    response = models.JSONField(blank=True, null=True)
    code = models.CharField(max_length=4, verbose_name='Код из СМС', blank=True)

    def update_sms_log(self, form_phone_number, seller_phone_number):
        if form_phone_number != seller_phone_number:
            self.confirmed = False
            self.save()

    def phone_verification_required(self):
        if self.seller.phone_number:
            return not self.confirmed
        return False

    class Meta:
        verbose_name = "SMSLog"
