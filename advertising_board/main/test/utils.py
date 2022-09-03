import os

from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import TemporaryUploadedFile

from main.models import Category, Ad, Tag


def create_ad(user):
    category = Category.objects.create(title='Авто', slug='auto')
    tag1 = Tag.objects.create(title='Авто с пробегом', slug='tag1')
    tag2 = Tag.objects.create(title='Продам тачку', slug='tag2')
    ad = Ad.objects.create(seller=user.seller, title="Продам Dodge", category=category)
    ad.tags.add(tag1, tag2)
    ad.save()
    return ad


class AdFormImageFormsetTestBase:
    def setUp(self):
        common_group = Group.objects.create(name='common_users')
        permission = Permission.objects.get(codename='add_ad')
        common_group.permissions.add(permission)
        user = get_user_model().objects.create_user(username="Джон Макклейн",
                                                    email='policerNewYourk@mail.com',
                                                    password='12345678')
        category = Category.objects.create(title='Мото', slug='moto')
        tag1 = Tag.objects.create(title='Продам мотоцикл', slug='tag1')
        tag2 = Tag.objects.create(title='Мотоцикл не дорого', slug='tag2')
        self.client.login(email='policerNewYourk@mail.com', password='12345678')
        self.data = {
            'imgs-TOTAL_FORMS': 4,
            'imgs-INITIAL_FORMS': 0,
            'imgs-MIN_NUM_FORMS': 0,
            'imgs-MAX_NUM_FORMS': 1000,
            'seller': user.id,
            'title': 'Honda crf250l',
            'description': 'Продам очень быстрый мотоцикл',
            'category': category.id,
            'tags': [tag1.id, tag2.id],
            'price': 2000,
            'type_ad': '1',
        }
        self.image_files = {}
        self.image_names = [
            'honda_crf_450_l.jpeg',
            '3175a6a86147a91f2cafdbe274082c55.jpg',
            'honda_crf_450_l.jpeg',
            '3175a6a86147a91f2cafdbe274082c55.jpg'
        ]
        self._add_data_to_form_ad_data()

    def _add_data_to_form_ad_data(self):
        imgs = [self._create_image(img) for img in self.image_names]
        for i, img in enumerate(imgs):
            self.image_files[f'imgs-{i}-img'] = img
            self.data[f'imgs-{i}-id'] = ''

    def _create_image(self, name):
        img_path = os.path.abspath(os.path.join(os.getcwd(), 'main', 'test', 'images', name))
        with open(img_path, 'rb') as f:
            upload_img = TemporaryUploadedFile(
                name=name,
                content_type='image/jpeg',
                size=os.path.getsize(img_path),
                charset='binary'
            )
            upload_img.write(f.read())
        return upload_img

    def _close_image_files(self):
        for img in self.image_files.values():
            img.close()
