from django.urls import path

from .views import (HomeView, ListAdView,
                    AdCreateView, AdUpdateView,
                    AdDetailView, RobotsTXTView)


app_name = 'main'
urlpatterns = [
    path('', HomeView.as_view(), name='home_url'),
    path('ads/', ListAdView.as_view(), name='list_ad_url'),
    path('ads/add', AdCreateView.as_view(), name='create_ad_url'),
    path('ads/<int:ad_id>/edit/', AdUpdateView.as_view(), name='update_ad_url'),
    path('ad/<int:ad_id>/', AdDetailView.as_view(), name='detail_ad_url'),
    path('robots.txt', RobotsTXTView.as_view())
]
