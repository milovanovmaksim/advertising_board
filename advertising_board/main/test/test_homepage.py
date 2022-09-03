from django.test import TestCase
from django.urls import reverse


class HomepageTest(TestCase):

    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url_name(self):
        response = self.client.get(reverse('main:home_url'))
        self.assertEqual(response.status_code, 200)
