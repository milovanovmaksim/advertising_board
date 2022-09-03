from django.shortcuts import redirect, render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django import forms

from .models import Ad
from accounts.models import Seller
from .forms import AdForm, ImageFormset


class CheckOwnerAdMixin(UserPassesTestMixin):
    permission_denied_message = "You don't have permission to edit someone else's Ad"

    def test_func(self):
        if self.request.user.has_perm('main.change_ad'):
            ad = super().get_object(queryset=self.queryset)
            return ad.seller == self.request.user.seller
        self.permission_denied_message = "You don't have permission to edit ad."
        return False


class AdCreateUpdateMixin():
    succes_message = None

    def get_form(self):
        if self.request.POST:
            ad_form = AdForm(self.request.POST, instance=self.object)
            image_formset = ImageFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            ad_form = AdForm(instance=self.object)
            image_formset = ImageFormset(instance=self.object)
        seller = Seller.objects.filter(seller=self.request.user)
        seller_model_choice = forms.ModelChoiceField(queryset=seller, label='Продавец')
        ad_form.fields['seller'] = seller_model_choice
        return ad_form, image_formset

    def form_valid(self, image_formset, ad_form):
        self.object = Ad.objects.create_or_update_ad(image_formset, ad_form)
        messages.success(self.request, self.succes_message)
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, image_formset, ad_form):
        return render(self.request, self.template_name, context=self.get_context_data())

    def get_context_data(self, **kwargs):
        ad_form, image_formset = self.get_form()
        context = {'form': ad_form, 'image_formset': image_formset}
        return context

    def post(self, request, *args, **kwargs):
        ad_form, image_formset = self.get_form()
        if ad_form.is_valid() and image_formset.is_valid():
            return self.form_valid(image_formset, ad_form)
        return self.form_invalid(image_formset, ad_form)
