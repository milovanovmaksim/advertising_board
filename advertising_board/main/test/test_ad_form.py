from django.test import TestCase
from django.urls import reverse

from .utils import AdFormImageFormsetTestBase
from main.forms import AdForm, ImageFormset


class AdFormTest(AdFormImageFormsetTestBase, TestCase):

    def test_ad_form_data_validation(self):
        ad_form = AdForm(self.data)
        self.assertTrue(ad_form.is_valid())

    def test_ad_form_seller_does_not_exist(self):
        self.data['seller'] = 2
        ad_form = AdForm(self.data)
        self.assertFalse(ad_form.is_valid())

    def test_ad_form_category_does_not_exist(self):
        self.data['category'] = 2
        ad_form = AdForm(self.data)
        self.assertFalse(ad_form.is_valid())

    def test_ad_form_tag_does_not_exist(self):
        self.data['tags'].append(3)
        ad_form = AdForm(self.data)
        self.assertFalse(ad_form.is_valid())

    def test_ad_form_detail_ad_url(self):
        ad_form = AdForm(self.data)
        ad = ad_form.save()
        self.assertEqual(ad.get_absolute_url(),
                         reverse("main:detail_ad_url", kwargs={"ad_id": ad.pk}))

    def test_count_ad_pictures(self):
        ad_form = AdForm(self.data)
        ad = ad_form.save()
        image_formset = ImageFormset(self.data, self.image_files, instance=ad)
        for form in image_formset:
            form.save()
        self._close_image_files()
        self.assertEqual(ad.imgs.count(), ImageFormset.extra)
