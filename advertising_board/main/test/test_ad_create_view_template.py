from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model


class AdCreateViewTemplateTest(TestCase):
    def setUp(self):
        common_group = Group.objects.create(name='common_users')
        permission = Permission.objects.get(codename='add_ad')
        common_group.permissions.add(permission)
        get_user_model().objects.create_user(username="Джон Макклейн",
                                             email='policerNewYourk@mail.com',
                                             password='12345678')
        self.client.login(email='policerNewYourk@mail.com', password='12345678')
        self.response = self.client.get(reverse('main:create_ad_url'))

    def test_ad_create_view_template(self):
        self.assertTemplateUsed(self.response, 'main/update_create_ad.html')

    def test_ad_create_view_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_ad_create_view_contains_correct_html(self):
        self.assertContains(self.response, 'Новое объявление')
