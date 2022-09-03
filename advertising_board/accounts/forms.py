from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import redis

from .models import Seller, SMSLog


CustomUser = get_user_model()


class UpdateUserForm(forms.ModelForm):
    custom_error_messages = {
        'user_already_exists': 'Пользователь с таки email уже зарегистрирован'
    }
    email = forms.CharField(required=True, error_messages={'required': 'Введите Ваш Email'},
                            validators=[validate_email],
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_record = CustomUser.objects.get_user_by_email(email=email)
        if not user_record or user_record.id == self.instance.id:
            return email
        raise ValidationError(self.custom_error_messages['user_already_exists'])


class UpdateSellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ('itn', 'phone_number')
        widgets = {
            'itn': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'})
        }

    def _check_itn(self, inn):
        if len(inn) not in (10, 12):
            return False

        def inn_csum(inn):
            k = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
            pairs = zip(k[11 - len(inn):], [int(x) for x in inn])
            return str(sum([k * v for k, v in pairs]) % 11 % 10)

        if len(inn) == 10:
            return inn[-1] == inn_csum(inn[:-1])
        else:
            return inn[-2:] == inn_csum(inn[:-2]) + inn_csum(inn[:-1])

    def clean_itn(self):
        itn = self.cleaned_data.get('itn')
        if not self._check_itn(itn):
            raise ValidationError('ИНН указан неверно')
        return itn


class SMSLogForm(forms.ModelForm):

    class Meta:
        model = SMSLog
        fields = ('code',)
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control mb-3', 'required': True})
        }

    def clean_code(self):
        form_code = self.cleaned_data.get('code')
        if not form_code:
            raise ValidationError('Обязательное поле для заполнения')
        redis_connection = redis.Redis(host='redis', port=6379, db=0)
        seller = self.instance.seller
        key = f'twilio_{seller.id}'
        code = redis_connection.get(key)
        if str(form_code) != code.decode("utf8"):
            raise ValidationError('Неверно указан код.')
        return form_code
