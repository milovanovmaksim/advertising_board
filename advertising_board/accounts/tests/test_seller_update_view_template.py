from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


class SellerUpdateViewTemplareTest(TestCase):

    def setUp(self):
        Group.objects.create(name='common_users')
        self.user = get_user_model().objects.create_user(username="Джон Макклейн",
                                                         email='policerNewYourk@mail.com',
                                                         password='12345678')

        self.client.login(email='policerNewYourk@mail.com', password='12345678')
        self.response = self.client.get(reverse('accounts:seller_url'))

    def test_seller_update_view_template(self):
        self.assertTemplateUsed(self.response, 'accounts/seller_update.html')

    def test_seller_update_view_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_seller_update_view_contains_correct_html(self):
        self.assertContains(self.response, 'Профиль')
