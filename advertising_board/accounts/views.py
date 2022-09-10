from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

from .forms import UpdateSellerForm, UpdateUserForm, SMSLogForm
from .models import SMSLog, Seller
from .utils import CodeTwilioSender
from .mixins import PhoneNumberAlreadyConfirmedMixin


class SellerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/seller_update.html'
    form_class = UpdateSellerForm
    login_url = '/accounts/login/'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.sms_log, _ = SMSLog.objects.get_or_create(seller=self.get_object())
        self.seller_phone_number = self.get_object().phone_number

    def get_object(self, queryset=None):
        return self.request.user.seller

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UpdateUserForm(instance=self.request.user)
        context['phone_verification_required'] = self.sms_log.phone_verification_required()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        seller_form = UpdateSellerForm(instance=self.object, data=self.request.POST)
        user_form = UpdateUserForm(instance=self.request.user, data=self.request.POST)
        if all([user_form.is_valid(), seller_form.is_valid()]):
            return self.form_valid(user_form, seller_form)
        return self.form_invalid(user_form, seller_form)

    def form_invalid(self, user_form, seller_form):
        context = {'user_form': user_form, 'form': seller_form}
        return render(self.request, self.template_name, context=context)

    def form_valid(self, user_form, seller_form):
        Seller.objects.update_seller(user_form, seller_form)
        form_phone_number = self.request.POST.get('phone_number')
        self.sms_log.update_sms_log(form_phone_number, self.seller_phone_number)
        messages.success(self.request, 'Данные успешно обновлены')
        return redirect('accounts:seller_url')


class SellerConfirmPhoneNumberView(PhoneNumberAlreadyConfirmedMixin,
                                   UpdateView):
    template_name = 'accounts/seller_confirm_phone_number.html'
    form_class = SMSLogForm

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.seller = self.request.user.seller

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phone_number'] = self.seller.phone_number
        return context

    def get_object(self, queryset=None):
        return SMSLog.objects.get(seller=self.seller)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        twilio = CodeTwilioSender(seller_id=self.seller.id)
        response = twilio.send_code_to_twilio()
        if response != 'Ok':
            messages.error(self.request, response)
            return redirect('accounts:seller_url')
        return render(request, self.template_name, context=context)

    def form_valid(self, form):
        self.object.confirmed = True
        self.object.save()
        messages.success(self.request, 'Номер телефона успешно подтвержден.')
        return redirect('accounts:seller_url')
