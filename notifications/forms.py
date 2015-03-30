# coding=utf-8

from django import forms
from django.contrib.auth.models import User


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
            raise forms.ValidationError("Пользователь с таким именем уже существует!")
