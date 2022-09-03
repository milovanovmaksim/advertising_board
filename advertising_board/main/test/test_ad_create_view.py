from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model


class AdCreateViewTest(TestCase):

    def setUp(self):
        self.common_group = Group.objects.create(name='common_users')
        permission = Permission.objects.get(codename='add_ad')
        self.common_group.permissions.add(permission)
        self.user = get_user_model().objects.create_user(username="Джон Макклейн",
                                                         email='policerNewYourk@mail.com',
                                                         password='12345678')

    def test_ad_create_view_status_code(self):
        response = self.client.get('/ads/add')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/ads/add')

        self.client.login(email='policerNewYourk@mail.com', password='12345678')
        response = self.client.get('/ads/add')
        self.assertEqual(response.status_code, 200)

        self.common_group.permissions.clear()
        response = self.client.get('/ads/add')
        self.assertEqual(response.status_code, 403)

    def test_detail_ad_url_name(self):
        self.client.login(email='policerNewYourk@mail.com', password='12345678')
        response = self.client.get(reverse('main:create_ad_url'))
        self.assertEqual(response.status_code, 200)
