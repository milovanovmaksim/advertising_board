from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.contrib import messages

from .models import Subscription
from .forms import SubscriptionForm


class SubscribeView(CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'subscription/subscription.html'

    def get_success_url(self):
        return reverse('subscription:subscribe_url')

    def form_valid(self, form):
        category = form.cleaned_data['category']
        self.subscribe(category)
        messages.success(self.request, f'Вы подписались на новые объявления, принадлежащие категории {category.title}')
        return redirect(self.get_success_url())

    def subscribe(self, category):
        if Subscription.objects.filter(category=category).exists():
            subs = Subscription.objects.get(category=category)
        else:
            subs = Subscription(category=category)
            subs.save()
        subs.users.add(self.request.user)
