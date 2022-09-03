from django.test import TestCase
from django.urls import reverse


class HomePageTemplateTest(TestCase):

    def setUp(self):
        url = reverse("main:home_url")
        self.response = self.client.get(url)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'main/index.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Home page')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')
