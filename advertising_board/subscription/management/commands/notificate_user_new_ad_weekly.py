from datetime import datetime

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from subscription.models import Subscription
from main.models import Ad


class NotificationUserNewAds():
    def __init__(self, time_zone, timedelta):
        self.time_zone = time_zone
        self.timedelta = timedelta
        self.start_date = datetime.now(self.time_zone) - self.timedelta
        self.end_date = datetime.now(self.time_zone)
        self.subscriptions = Subscription.objects.all()
        self.ads = None

    def create_messages(self):
        messages = []
        for subscription in self.subscriptions:
            users = subscription.users.all()
            subject = f'Новое объявление в категории {subscription.category.title}'
            if users:
                for user in users:
                    message = self.create_message(user, subscription, subject)
                    if message:
                        messages.append(message)
        return messages

    def create_message(self, user, subscription, subject):
        message = None
        html_content = self.get_html_content(subscription, user)
        if html_content:
            message = EmailMessage(subject=subject, body=html_content, to=[user.email])
            message.content_subtype = 'html'
        return message

    def run(self):
        messages = self.create_messages()
        for message in messages:
            message.send()
        print('Сообщения отправлены')

    def get_context_data(self, subscription, user):
        category = subscription.category
        self.ads = Ad.objects.filter(created_at__range=[self.start_date, self.end_date],
                                     category=category).exclude(seller=user.seller)
        context = {'category': category, 'ads': self.ads, 'user': user, 'SITE_URL': settings.SITE_URL}
        return context

    def get_html_content(self, subscription, user):
        context = self.get_context_data(subscription, user)
        html_content = None
        if self.ads:
            html_content = render_to_string('subscription/notification.html', context)
            return html_content
        return html_content
