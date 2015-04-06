# coding=utf-8

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug, RegexValidator
from notifications import models

class LoginForm(forms.Form):
    login = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    login = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    duplicate_password = forms.CharField(label="Пароль ещё раз", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if cleaned_data["password"] != cleaned_data["duplicate_password"]:
            raise forms.ValidationError("Введённые пароли не совпадают!")
        if User.objects.filter(username=cleaned_data["login"]).count() != 0:
            raise forms.ValidationError("Пользователь с таким логином уже существует!")

class CreateApplicationForm(forms.Form):
    name = forms.CharField(label="Название приложения")
    description = forms.CharField(label="Краткое описание, для каких рассылок приложение"
                                        " используется (не более 300 символов)", widget=forms.Textarea,
                                  max_length=300)
    image = forms.FileField(label="Ваш логотип (отображается при старте приложения)")
    key = forms.ModelChoiceField(label="Ключ для подписи приложения", queryset=models.AppKey.objects.all(),
                                 required=False)

class CreateApplicationKeyForm(forms.ModelForm):

    duplicate_alias_password = forms.CharField(label="Повторите пароль алиаса", widget=forms.PasswordInput)
    duplicate_key_password = forms.CharField(label="Повторите пароль ключа", widget=forms.PasswordInput)

    class Meta:
        model = models.AppKey
        fields = (
            "org_unit", "org_name", "city", "province", "country_code",
            "alias_name", "alias_password", "duplicate_alias_password",
            "key_password", "duplicate_key_password",
        )
        labels = {
            "alias_name": "Название ключа (алиас)",
            "key_password": "Пароль ключа",
            "org_unit": "Организационный юнит",
            "org_name": "Название организации",
            "city": "Город",
            "province": "Область/Регион",
            "country_code": "Код страны",
            "alias_password": "Пароль для алиаса",
        }
        widgets = {
            "key_password": forms.PasswordInput,
            "alias_password": forms.PasswordInput,
        }

    def clean_alias_name(self):
        value = self.cleaned_data['alias_name']
        if models.AppKey.objects.filter(alias_name=value).count() > 0:
            raise ValidationError("Ключ с таким алиасом уже существует!")
        return value

    def clean(self):
        cleaned_data = super(CreateApplicationKeyForm, self).clean()
        for field in cleaned_data:
            if field in ["country_code"]: continue
            RegexValidator("^[\da-zA-Z_-]+$", "Используйте только латинские буквы, подчёркивание и дефис!")(cleaned_data[field])
        if "alias_password" in cleaned_data and "duplicate_alias_password" in cleaned_data:
            if cleaned_data["alias_password"] != cleaned_data["duplicate_alias_password"]:
                raise ValidationError("Пароли для алиаса не совпадают!")
        if "key_password" in cleaned_data and "duplicate_key_password" in cleaned_data:
            if cleaned_data["key_password"] != cleaned_data["duplicate_key_password"]:
                raise ValidationError("Пароли для ключа не совпадают!")

class CreateThemeForm(forms.ModelForm):
    class Meta:
        model = models.Theme
        fields = ("name",)
        labels = {
            "name": "Создать новую рассылку",
        }

class CreateMessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ("text", "url", )
        labels = {
            "text": "Текст сообщения",
            "url": "Ссылка для перехода (не обязательно)",
        }
    def __init__(self, *args, **kwargs):
        super(CreateMessageForm, self).__init__(*args, **kwargs)
        if "url" in self.fields:
            self.fields["url"].required = False