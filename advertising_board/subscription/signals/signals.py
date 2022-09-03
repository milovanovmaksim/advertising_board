from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task

from main.models import Ad
from ..models import Subscription


CustomUser = settings.AUTH_USER_MODEL


@receiver(post_save, sender=Ad)
def notificate_user_new_ad(sender, instance, created, **kwargs):
    if created:
        notificate.delay(id_ad=instance.id)


@shared_task
def notificate(id_ad):
    try:
        ad = Ad.objects.get(id=id_ad)
    except Ad.DoesNotExist:
        return
    if Subscription.objects.filter(category=ad.category).exists():
        subscription = Subscription.objects.get(category=ad.category)
        users = subscription.users.all()
        if users:
            subject = f'Новое объявление в категории {ad.category.title}'
            message = (f'Вы подписывались на рассылку новых'
                       'объявлений, принадлежащих категории "{ad.category.title}"\n'
                       f'Новое объявление доступно по ссылке {settings.SITE_URL}{ad.get_absolute_url()}')
            recipient_list = [user.email for user in users if not (user.seller == ad.seller)]
            send_mail(subject=subject, message=message,
                      from_email=None, recipient_list=recipient_list)
