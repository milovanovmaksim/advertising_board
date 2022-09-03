from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import Seller, SMSLog


CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username']


class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'get_number_ads')
    readonly_fields = ('get_number_ads', )

    def get_number_ads(self, obj):
        return obj.number_ads

    get_number_ads.short_description = 'Кол-во объявлений'


class SMSLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'confirmed')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(SMSLog, SMSLogAdmin)
