from django.urls import path

from .views import SubscribeView


app_name = 'subscription'

urlpatterns = [
    path('subscribe/', SubscribeView.as_view(), name='subscribe_url'),
    # path('unsubscribe/', UnsubscribeView.as_view(), name='unsubscribe_url'),
]