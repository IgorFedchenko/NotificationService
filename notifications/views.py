from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from notifications.forms import LoginForm, RegistrationForm


def main(request):
    login_form = LoginForm()
    return render(request, "notifications/main.html", { "login_form": login_form } )

@login_required()
def logout_view(request):
    logout(request)
    return redirect(reverse("main"))

class Registration(View):

    def get(self, request):
        if request.user.is_authenticated():
            return redirect(reverse("main"))
        registration_form = RegistrationForm()
        return render(request, "notifications/registration.html", { "registration_form": registration_form } )

    def post(self, request):
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            username = registration_form.cleaned_data['login']
            password = registration_form.cleaned_data["password"]
            user = User.objects.create_user(username, password=password)
            user.first_name = registration_form.cleaned_data['first_name']
            user.last_name = registration_form.cleaned_data['last_name']
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse("account", args=[user.id]))
        return render(request, "notifications/registration.html", { "registration_form": registration_form } )

class Account(View):

    @method_decorator(login_required)
    def get(self, request, pk):
        if request.user.id != int(pk):
            print request.user.id
            print int(pk)
            return redirect(reverse("main"))
        return render(request, "notifications/account.html")

@login_required()
def create_app(request):
    pass

@login_required()
def create_app_key(request):
    pass

@login_required()
def create_theme(request):
    pass

@login_required()
def app_details(request, pk):
    pass

@login_required()
def theme_details(request, pk):
    pass

@login_required()
def message_details(request, pk):
    pass

