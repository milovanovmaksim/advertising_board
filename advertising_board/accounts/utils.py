from random import randint

from django.conf import settings

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import redis

from .models import Seller


class CodeTwilioSender:
    ACCOUNT_SID = settings.ACCOUNT_SID
    AUTH_TOKEN = settings.AUTH_TOKEN
    MESSAGING_SERVICE_SID = settings.MESSAGING_SERVICE_SID
    ERROR_MESSAGE = 'Ошибка при отправке кода подтверждения на номер телефона {phone_number}'

    def __init__(self, seller_id):
        self.seller_id = seller_id
        self.seller = Seller.objects.get(id=self.seller_id)
        self.phone_number = self.seller.phone_number
        self.redis_connection = redis.Redis(host='redis', port=6379, db=0)
        self.client = Client(self.ACCOUNT_SID, self.AUTH_TOKEN)

    def send_code_to_twilio(self):
        code = f"{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}"
        key = f'twilio_{self.seller_id}'
        self.redis_connection.set(key, code)
        self.redis_connection.expire(self.seller_id, 120)
        try:
            self.client.messages.create(messaging_service_sid=self.MESSAGING_SERVICE_SID,
                                        body=code,
                                        to=self.phone_number)
        except TwilioRestException:
            # print(self.client.http_client.last_response.content)
            # print(exc.__dict__)
            return self.ERROR_MESSAGE.format(phone_number=self.phone_number)
        return 'Ok'
