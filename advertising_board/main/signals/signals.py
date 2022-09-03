
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from ..models import Tag, Ad


@receiver(post_save, sender=Tag)
def tag_post_save_handler(sender, instance, created, **kwargs):
    key = make_template_fragment_key('tags')
    cache.delete(key)


@receiver(post_save, sender=Ad)
def ad_post_save_handler(sender, instance, created, **kwargs):
    key = f'ad_id={instance.pk}'
    cache.delete(key)
