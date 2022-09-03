from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .utils import create_ad


class AdDetailTest(TestCase):

    def setUp(self):
        Group.objects.create(name='common_users')
        user = get_user_model().objects.create_user(username="Джон Макклейн",
                                                    email='policerNewYourk@mail.com',
                                                    password='12345678')
        self.ad = create_ad(user)
        self.response = self.client.get(f'/ad/{self.ad.id}/')
        self.response_with_404 = self.client.get('/ad/2/')

    def test_detail_ad_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response_with_404.status_code, 404)

    def test_detail_ad_url_name(self):
        response = self.client.get(reverse('main:detail_ad_url', kwargs={'ad_id': self.ad.id}))
        self.assertEqual(response.status_code, 200)

    def test_detail_ad_context(self):
        self.assertEqual(self.response.context.get('ad'), self.ad)

    def test_caching_detail_ad(self):
        key = f"ad_id={self.ad.id}"
        cached_ad = cache.get(key)
        self.assertEqual(self.ad, cached_ad)
        self.ad.title = 'Продам Ferrari'
        self.ad.save()
        self.assertEqual(cache.get(key), None)
