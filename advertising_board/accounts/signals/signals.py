from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import Group

from accounts.models import Seller


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_seller(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='common_users'))
        Seller.objects.create(seller=instance)
