from django.test import TestCase
from django.urls import reverse


class ListAdViewTest(TestCase):

    def test_list_ad_view_status_code(self):
        response = self.client.get('/ads/')
        self.assertEqual(response.status_code, 200)

    def test_list_ad_view_url_name(self):
        response = self.client.get(reverse('main:list_ad_url'))
        self.assertEqual(response.status_code, 200)
