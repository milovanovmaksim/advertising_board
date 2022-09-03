from datetime import datetime, timedelta
import zoneinfo

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from celery import Task, shared_task, group

from config.celery import app
from .models import Subscription
from main.models import Ad


class NotificationUserNewAds(Task):
    start_date = None
    end_date = None
    ads = None

    def create_messages(self):
        attributes = []
        subscriptions = Subscription.objects.all()
        for subscription in subscriptions:
            users = subscription.users.all()
            subject = f'Новое объявление в категории {subscription.category.title}'
            if users:
                for user in users:
                    data = self.get_email_object_kwargs(user, subscription, subject)
                    if data:
                        attributes.append(data)
        return attributes

    def get_email_object_kwargs(self, user, subscription, subject):
        data = None
        html_content = self.get_html_content(subscription, user)
        if html_content:
            data = {'subject': subject, 'body': html_content, 'to': [user.email]}
        return data

    def run(self, delta):
        time_zone = zoneinfo.ZoneInfo(settings.TIME_ZONE)
        self.end_date = datetime.now(time_zone)
        self.start_date = datetime.now(time_zone) - timedelta(**delta)
        attributes = self.create_messages()
        group([self.send_message.s(**data) for data in attributes]).apply_async()
        print("Сообщения отправлены")

    def get_context_data(self, subscription, user):
        category = subscription.category
        self.ads = Ad.objects.filter(created_at__range=[self.start_date, self.end_date],
                                     category=category).exclude(seller=user.seller)
        context = {'category': category, 'ads': self.ads,
                   'user': user, 'SITE_URL': settings.SITE_URL,
                   'end_date': self.end_date, 'start_date': self.start_date}
        return context

    def get_html_content(self, subscription, user):
        context = self.get_context_data(subscription, user)
        html_content = None
        if self.ads:
            html_content = render_to_string('subscription/notification.html', context)
            return html_content
        return html_content

    @staticmethod
    @shared_task
    def send_message(**kwargs):
        message = EmailMessage(**kwargs)
        message.content_subtype = 'html'
        message.send()


app.register_task(NotificationUserNewAds())

"""
class MyTask(object):
    def __init__(self, *args, **kwargs): pass

    def run(self): pass

@shared_task(bind=True)
def my_task(self, *args, **kwargs):
    MyTask(*args, **kwargs).run()
"""
