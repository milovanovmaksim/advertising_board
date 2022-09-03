from django.urls import path

from .views import SellerConfirmPhoneNumberView, SellerUpdateView

app_name = 'accounts'
urlpatterns = [

    # profile
    path('seller/', SellerUpdateView.as_view(), name='seller_url'),
    path('seller/confirm-phone-number/', SellerConfirmPhoneNumberView.as_view(), name='confirm_phone_number_url')

]