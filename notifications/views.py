from StringIO import StringIO
import mimetypes
import os
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View

from django_tables2 import RequestConfig
from django_ajax.mixin import AJAXMixin
from django_ajax.decorators import ajax

from notifications import forms, models, tables

class Main(View):

    def get(self, request):
        login_form = forms.LoginForm()
        return render(request, "notifications/main.html", { "login_form": login_form } )

    def post(self, request):
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data["login"],
                                password=login_form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect(reverse("account", args=[user.id]))
        return render(request, "notifications/main.html", { "login_form": login_form } )

@login_required()
def logout_view(request):
    logout(request)
    return redirect(reverse("main"))

class Registration(View):

    def get(self, request):
        if request.user.is_authenticated():
            return redirect(reverse("main"))
        registration_form = forms.RegistrationForm()
        print render(request, "notifications/registration.html")
        return render(request, "notifications/registration.html", { "registration_form": registration_form } )

    def post(self, request):
        registration_form = forms.RegistrationForm(request.POST)
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
            return redirect(reverse("main"))
        applications_table = tables.ApplicationsTable(models.MobileApp.objects.filter(user=request.user))
        RequestConfig(request).configure(applications_table)
        return render(request, "notifications/account.html",
                      {"applications_table" : applications_table,})

class CreateApplication(View):

    @method_decorator(login_required)
    def get(self, request):
        create_application_form = forms.CreateApplicationForm()
        return render(request, "notifications/create_app.html", {"create_application_form" : create_application_form})

    @method_decorator(login_required)
    def post(self, request):
        create_application_form = forms.CreateApplicationForm(request.POST ,request.FILES)
        if create_application_form.is_valid():
            models.MobileApp.objects.create(
                user = request.user,
                name = create_application_form.cleaned_data["name"],
                description = create_application_form.cleaned_data["description"],
                image = create_application_form.cleaned_data["image"],
                key = create_application_form.cleaned_data["key"],
                creation_date = timezone.now(),
            )
            return redirect(reverse("account", args=[request.user.id]))
        return render(request, "notifications/create_app.html", { "create_application_form": create_application_form} )

class ApplicationKeysManage(View):
    def get_keys_table(self, request):
        application_keys_table = tables.ApplicationKeysTable(models.AppKey.objects.filter(user=request.user))
        RequestConfig(request).configure(application_keys_table)
        return application_keys_table

    #@method_decorator(ajax)
    @method_decorator(login_required)
    def post(self, request):
        if 'delete_id' in request.POST:
            app_key = get_object_or_404(models.AppKey, pk=request.POST.get('delete_id'))
            if app_key.user == request.user:
                app_key.delete()
            return None
        application_keys_table = self.get_keys_table(request)
        app_key = models.AppKey(user=request.user, creation_date = timezone.now())
        create_app_key_form = forms.CreateApplicationKeyForm(request.POST, instance=app_key)
        if create_app_key_form.is_valid():
            create_app_key_form.save()
            create_app_key_form = forms.CreateApplicationKeyForm()
        return render(request, "notifications/app_keys_manage.html",
                      {"create_app_key_form": create_app_key_form,
                       "application_keys_table": application_keys_table,})

    @method_decorator(login_required)
    def get(self, request):
        application_keys_table = self.get_keys_table(request)
        create_app_key_form = forms.CreateApplicationKeyForm()
        return render(request, "notifications/app_keys_manage.html",
                      {"create_app_key_form": create_app_key_form,
                       "application_keys_table": application_keys_table,})

class ApplicationDetails(View):

    def get_themes_table(self, request, app_id):
        themes_table = tables.ThemesTable(models.Theme.objects.filter(user=request.user,
                                                                      application=models.MobileApp.objects.get(pk=app_id)))
        RequestConfig(request).configure(themes_table)
        return themes_table

    #@method_decorator(ajax)
    @method_decorator(login_required)
    def post(self, request, pk):
        if 'delete_id' in request.POST:
            theme = get_object_or_404(models.Theme, pk=request.POST.get('delete_id'))
            if theme.user == request.user:
                theme.delete()
            return HttpResponse()
        theme = models.Theme(user=request.user, creation_date=timezone.now(),
                             application=models.MobileApp.objects.get(pk=pk))
        create_theme_form = forms.CreateThemeForm(request.POST, instance=theme)
        if create_theme_form.is_valid():
            create_theme_form.save()
            return self.get(request, pk)
        themes_table = self.get_themes_table(request, pk)
        return render(request, "notifications/app_details.html",
                        {
                            "create_theme_form": create_theme_form,
                            "themes_table": themes_table,
                        })

    @method_decorator(login_required)
    def get(self, request, pk):
        create_theme_form = forms.CreateThemeForm()
        themes_table = self.get_themes_table(request, pk)
        return render(request, "notifications/app_details.html",
                        {
                            "create_theme_form": create_theme_form,
                            "themes_table": themes_table,
                        })

class ThemeDetails(View):
    def get_messages_table(self, request, pk):
        messages_table = tables.MessagesTable(models.Message.objects.filter(theme=models.Theme.objects.get(pk=pk)))
        RequestConfig(request).configure(messages_table)
        return messages_table

    @method_decorator(login_required)
    def post(self, request, pk):
        messages_table = self.get_messages_table(request, pk)
        message = models.Message(theme=models.Theme.objects.get(pk=pk), creation_date=timezone.now())
        create_message_form = forms.CreateMessageForm(request.POST, instance=message)
        if create_message_form.is_valid():
            create_message_form.save()
            return self.get(request, pk)
        return render(request, "notifications/theme_details.html",
            {
                "messages_table": messages_table,
                "create_message_form": create_message_form,
            })

    @method_decorator(login_required)
    def get(self, request, pk):
        messages_table = self.get_messages_table(request, pk)
        create_message_form = forms.CreateMessageForm()
        return render(request, "notifications/theme_details.html",
            {
                "messages_table": messages_table,
                "create_message_form": create_message_form,
            })

class MessageDetails(View):

    @method_decorator(login_required)
    def get(self, request, pk):
        return render(request, "notifications/message_details.html")

@login_required()
def delete_app(request, pk):
    pass

@login_required()
def delete_theme(request, pk):
    pass

@login_required()
def delete_app_key(request, pk):
    pass

class DownloadApplication(View):

    def response_by_filepath(self, path):
        filename = path.split('/')[-1]
        file = StringIO(open(path, "rb").read())
        mimetype = mimetypes.guess_type(os.path.basename(path))[0]
        response = HttpResponse(file, content_type='application/%s'%str(mimetype))
        response['Content-Disposition'] = 'attachment; filename="%s"'%filename
        return response

    #@method_decorator(ajax)
    @method_decorator(login_required)
    def post(self, request, pk, hash):
        return "hash4545sum"

    @method_decorator(login_required)
    def get(self, request, pk, hash = None):
        if hash is not None:
            link = "media/file.bin"
            return self.response_by_filepath(link)
        return render(request, "notifications/download_app.html")
