from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import PasswordInput, ModelForm
from django.core.validators import validate_email
from django.forms import ModelForm
from django.forms import Textarea
# forms.py
from django import forms


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.TextInput(attrs={'class': 'quantity-input'}))


# форма авторизации
class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Username')
    password = forms.CharField(required=True, label='Пароль')


# форма регистрации
class RegisterForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    username = forms.CharField(min_length=3, max_length=10, required=True, label='Никнейм', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='Может содержать только латинские буквы и цифры',
            code='invalid_username'
        ),
    ])

    email = forms.CharField(min_length=3, required=True, label='Email')

    password = forms.CharField(widget=PasswordInput(), required=True, label='Пароль')
    password_confirm = forms.CharField(widget=PasswordInput(), required=True, label='Повторите пароль')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        # валидация паролей
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                {'password_confirm': "Пароли не совпадают", 'password': ''}
            )
        # валидация никнейма
        username = self.cleaned_data.get("username")

        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError({'username': "Такой логин уже занят"})

        # валидация email
        try:
            validate_email(self.cleaned_data.get("email"))
        except ValidationError as e:
            raise forms.ValidationError({'email': "Email не является валидным адресом"})

        return cleaned_data


# Svaz'
class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea,
                              max_length=2000)


class ProductSearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_query'}))
    min_price = forms.DecimalField(label='Минимальная цена', required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_min_price'}))
    max_price = forms.DecimalField(label='Максимальная цена', required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_max_price'}))


class PriceFilterForm(forms.Form):
    min_price = forms.DecimalField(label='Минимальная цена', required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_min_price'}))
    max_price = forms.DecimalField(label='Максимальная цена', required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_max_price'}))
