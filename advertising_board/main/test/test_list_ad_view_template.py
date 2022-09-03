from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from .utils import create_ad


class ListAdViewTemplateTest(TestCase):

    def setUp(self):
        Group.objects.create(name='common_users')
        user = get_user_model().objects.create_user(username="Джон Макклейн",
                                                    email='policerNewYourk@mail.com',
                                                    password='12345678')
        self.ad = create_ad(user)
        url = reverse("main:list_ad_url")
        self.response = self.client.get(url)

    def test_list_ad_view_template(self):
        self.assertTemplateUsed(self.response, 'main/ad_list.html')

    def test_list_ad_view_contains_correct_html(self):
        self.assertContains(self.response, self.ad.title)

    def test_list_ad_view_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_caching_template_fragment_tags(self):
        key = make_template_fragment_key('tags')
        tags = cache.get(key)
        self.assertContains(self.response, tags)
