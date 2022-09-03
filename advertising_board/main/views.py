import socket

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.http import HttpResponse

from .models import Ad
from .forms import AdForm
from .mixins import CheckOwnerAdMixin, AdCreateUpdateMixin


class HomeView(View):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        id = socket.gethostname
        return render(request, self.template_name, context={'id': id})


class ListAdView(ListView):
    model = Ad
    template_name = 'main/ad_list.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        slug_tag = self.request.GET.get('tag')
        page_number = self.request.GET.get('page')
        page_ads = Ad.objects.get_page_objects(page_number=page_number, slug_tag=slug_tag)
        return page_ads


class AdDetailView(DetailView):
    model = Ad
    template_name = 'main/ad_detail.html'
    context_object_name = 'ad'
    pk_url_kwarg = 'ad_id'

    def get_object(self, queryset=None):
        ad_id = self.kwargs.get('ad_id')
        key = f"ad_id={ad_id}"
        ad = cache.get(key)
        if not ad:
            ad = get_object_or_404(Ad, pk=ad_id)
            cache.set(key, ad)
        return ad


class AdCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                   AdCreateUpdateMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'main/update_create_ad.html'
    succes_message = 'Объявление успешно создано.'
    login_url = '/accounts/login/'
    permission_required = ('main.add_ad', )
    permission_denied_message = "You don't have permission to add ad."

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creation'] = True
        return context


class AdUpdateView(LoginRequiredMixin, CheckOwnerAdMixin,
                   AdCreateUpdateMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'main/update_create_ad.html'
    pk_url_kwarg = 'ad_id'
    succes_message = 'Объявление успешно обновлено.'
    login_url = '/accounts/login/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class RobotsTXTView(View):
    http_method_names = ['get']

    def get(self, request):
        lines = [
            "User-Agent: *",
            "Disallow: /seller/",
            "Disallow: /seller/confirm-phone-number/",
        ]
        return HttpResponse("\n".join(lines), content_type="text/plain")
