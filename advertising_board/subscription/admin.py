from django.contrib import admin

from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')
    list_display_links = ('id', )
    search_fields = ('users__username', 'category__title')
    list_filter = ['users', 'category']


admin.site.register(Subscription, SubscriptionAdmin)
