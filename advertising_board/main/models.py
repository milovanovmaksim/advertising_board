from django.db import models
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from sorl.thumbnail import ImageField, delete

from accounts.models import Seller


class BaseModel(models.Model):
    """ Base model class.

    :param title: Ad title
    :type models: class: models.CharField
    """
    title = models.CharField(max_length=100, verbose_name='Заголовок')

    class Meta:
        abstract = True


class Category(BaseModel):
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')

    class Meta:
        ordering = ('-title',)
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.title}'


class Tag(BaseModel):
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')

    class Meta:
        ordering = ('-title',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'Тэг: {self.title}'


class AdType(models.IntegerChoices):
    archived = 0, 'АРХИВИРОВАННОЕ'
    not_archived = 1, 'НЕАРХИВИРОВАННОЕ'


class AdCustomManager(models.Manager):
    def get_page_objects(self, page_number, slug_tag=None):
        queryset = []
        if slug_tag:
            tag = get_object_or_404(Tag, slug=slug_tag)
            queryset = self.get_by_tag(tag)
        else:
            queryset = self.all()
        pagintator = Paginator(queryset, 10)
        page_ads = pagintator.get_page(page_number)
        return page_ads

    def get_by_tag(self, tag):
        return self.filter(tags__slug=tag.slug)

    def create_or_update_ad(self, image_formset, ad_form):
        ad = ad_form.save()
        image_formset.instance = ad
        image_formset.save()
        return ad

    def search_ads(self, message):
        result = set()
        ads = []
        if message:
            ads_by_title = list(self.filter(title__icontains=message))
            ads_by_description = list(self.filter(description__icontains=message))
            result.update(set(ads_by_title), set(ads_by_description))
            if result:
                ads = [{'title': ad.title, 'url': ad.get_absolute_url()} for ad in result]
        return ads


class Ad(BaseModel):
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey(Category, related_name='ads', on_delete=models.CASCADE, verbose_name='Категория')
    seller = models.ForeignKey(Seller, related_name='ads', on_delete=models.CASCADE, verbose_name='Продавец')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    tags = models.ManyToManyField(Tag, related_name='ads', verbose_name='Тэги')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    type_ad = models.IntegerField(choices=AdType.choices, default=AdType.not_archived, verbose_name='Тип  объявления')

    objects = AdCustomManager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return f'Объявление: {self.title}; Категория: {self.category}'

    def get_absolute_url(self):
        return reverse("main:detail_ad_url", kwargs={"ad_id": self.pk})


class ArchivedAdsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type_ad=AdType.archived)


class ArchiveAds(Ad):
    objects = ArchivedAdsManager()

    class Meta:
        proxy = True
        verbose_name = "Архивное объявление"
        verbose_name_plural = "Архивные объявления"


class Picture(models.Model):
    img = ImageField(upload_to="ads/%Y/%m/%d/", verbose_name='Фото')
    ad = models.ForeignKey(Ad, related_name='imgs', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def _remove_on_update_image(self):
        try:
            old_img = Picture.objects.get(id=self.id)
        except Picture.DoesNotExist:
            return
        if self.img and old_img.img and self.img != old_img:
            delete(old_img.img.path)

    def save(self, *args, **kwargs):
        self._remove_on_update_image()
        return super().save(*args, **kwargs)
