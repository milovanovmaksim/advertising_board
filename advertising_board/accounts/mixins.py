from django.contrib import messages
from django.shortcuts import redirect


class PhoneNumberAlreadyConfirmedMixin:

    def dispatch(self, request, *args, **kwargs):
        sms_log = self.get_object()
        if sms_log.confirmed:
            return PhoneNumberAlreadyConfirmedMixin.get(self, request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.info(request, 'Ваш номер телефон уже подтвержден.')
        return redirect('accounts:seller_url')
