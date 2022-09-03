from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


class SellerUpdateViewTest(TestCase):
    def setUp(self):
        Group.objects.create(name='common_users')
        self.user = get_user_model().objects.create_user(username="Джон Макклейн",
                                                         email='policerNewYourk@mail.com',
                                                         password='12345678')

    def test_seller_update_view_status_code(self):
        response = self.client.get('/accounts/seller/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/seller/')

        self.client.login(email='policerNewYourk@mail.com', password='12345678')
        response = self.client.get('/accounts/seller/')
        self.assertEqual(response.status_code, 200)

    def test_seller_update_ad_url_name(self):
        self.client.login(email='policerNewYourk@mail.com', password='12345678')
        response = self.client.get(reverse('accounts:seller_url'))
        self.assertEqual(response.status_code, 200)
