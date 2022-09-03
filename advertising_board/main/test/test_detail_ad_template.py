from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .utils import create_ad


class DetailAdTemplateTest(TestCase):
    def setUp(self):
        Group.objects.create(name='common_users')
        user = get_user_model().objects.create_user(username="Джон Макклейн",
                                                    email='policerNewYourk@mail.com',
                                                    password='12345678')
        self.ad = create_ad(user)
        self.response = self.client.get(reverse('main:detail_ad_url', kwargs={'ad_id': self.ad.id}))

    def test_detail_ad_view_template(self):
        self.assertTemplateUsed(self.response, 'main/ad_detail.html')

    def test_detail_ad_view_contains_correct_html(self):
        self.assertContains(self.response, self.ad.title)

    def test_detail_ad_view_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')
