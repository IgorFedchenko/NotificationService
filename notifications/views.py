# coding=utf-8
from StringIO import StringIO
import mimetypes
import os
import subprocess
import shutil
import logging

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

from NotificationService.settings import BASE_DIR, MEDIA_ROOT

from notifications import forms, models, tables

import pexpect


class Main(View):

    def add_breadcrumbs(self, request):
        request.breadcrumbs([
            ("Главная", reverse("main")),
        ])

    def get(self, request):
        self.add_breadcrumbs(request)
        login_form = forms.LoginForm()
        return render(request, "notifications/main.html", { "login_form": login_form } )

    def post(self, request):
        self.add_breadcrumbs(request)
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

    def add_breadcrumbs(self, request):
        request.breadcrumbs([
            ("Главная", reverse("main")),
            ("Регистрация", reverse("registration")),
        ])

    def get(self, request):
        self.add_breadcrumbs(request)
        if request.user.is_authenticated():
            return redirect(reverse("main"))
        registration_form = forms.RegistrationForm()
        return render(request, "notifications/registration.html", { "registration_form": registration_form } )

    def post(self, request):
        self.add_breadcrumbs(request)
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
    def add_breadcrumbs(self, request):
        request.breadcrumbs([
            ("Главная", reverse("main")),
            ("Личный кабинет", reverse("account", args=[request.user.id])),
        ])

    @method_decorator(login_required)
    def get(self, request, pk):
        self.add_breadcrumbs(request)
        applications_table = tables.ApplicationsTable(models.MobileApp.objects.filter(user=request.user))
        RequestConfig(request).configure(applications_table)
        return render(request, "notifications/account.html",
                      {"applications_table" : applications_table,})

class CreateApplication(View):
    def add_breadcrumbs(self, request):
       request.breadcrumbs([
           ("Главная", reverse("main")),
           ("Личный кабинет", reverse("account", args=[request.user.id])),
           ("Создание приложения", reverse("create_app")),
       ])

    @method_decorator(login_required)
    def get(self, request):
        self.add_breadcrumbs(request)
        create_application_form = forms.CreateApplicationForm(user=request.user)
        return render(request, "notifications/create_app.html", {"create_application_form" : create_application_form})

    @method_decorator(login_required)
    def post(self, request):
        self.add_breadcrumbs(request)
        create_application_form = forms.CreateApplicationForm(request.POST ,request.FILES, user=request.user)
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

    def add_breadcrumbs(self, request):
       request.breadcrumbs([
           ("Главная", reverse("main")),
           ("Личный кабинет", reverse("account", args=[request.user.id])),
           ("Управление ключами приложений", reverse("app_keys_manage")),
       ])

    def get_keys_table(self, request):
        application_keys_table = tables.ApplicationKeysTable(models.AppKey.objects.filter(user=request.user))
        RequestConfig(request).configure(application_keys_table)
        return application_keys_table

    @method_decorator(login_required)
    def post(self, request):
        self.add_breadcrumbs(request)
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
        self.add_breadcrumbs(request)
        application_keys_table = self.get_keys_table(request)
        create_app_key_form = forms.CreateApplicationKeyForm()
        return render(request, "notifications/app_keys_manage.html",
                      {"create_app_key_form": create_app_key_form,
                       "application_keys_table": application_keys_table,})

class ApplicationDetails(View):

    def add_breadcrumbs(self, request, pk):
        app = models.MobileApp.objects.get(pk=pk)
        request.breadcrumbs([
            ("Главная", reverse("main")),
            ("Личный кабинет", reverse("account", args=[request.user.id])),
            (u"Приложение '%s'"%app.name, reverse("app_details", args=[pk])),
        ])

    def get_themes_table(self, request, app_id):
        themes_table = tables.ThemesTable(models.Theme.objects.filter(user=request.user,
                                                                      application=models.MobileApp.objects.get(pk=app_id)))
        RequestConfig(request).configure(themes_table)
        return themes_table

    @method_decorator(login_required)
    def post(self, request, pk):
        self.add_breadcrumbs(request, pk)
        if 'delete_id' in request.POST:
            theme = get_object_or_404(models.Theme, pk=request.POST.get('delete_id'))
            if theme.user == request.user:
                theme.messages.all().delete()
                theme.delete()
            return HttpResponse()
        elif 'change_key_form_submit' in request.POST:
            change_key_form = forms.ChangeApplicationKeyForm(request.POST)
            if change_key_form.is_valid():
                app = models.MobileApp.objects.get(pk=pk)
                app.key=change_key_form.cleaned_data["key"]
                app.save()
                return self.get(request, pk)
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
        self.add_breadcrumbs(request, pk)
        application = models.MobileApp.objects.get(pk=pk)
        create_theme_form = forms.CreateThemeForm()
        themes_table = self.get_themes_table(request, pk)
        change_app_key_form = forms.ChangeApplicationKeyForm(user=request.user)
        return render(request, "notifications/app_details.html",
                        {
                            "create_theme_form": create_theme_form,
                            "themes_table": themes_table,
                            "application": application,
                            "change_app_key_form": change_app_key_form,
                        })

class ThemeDetails(View):
    def send_message(self, message):
        import json, httplib
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        request = {
            "where": {
                "deviceType": "android",
                "appID": "%i"%message.theme.application.id,
            },
            "data": {
                "alert": message.text,
                "title": message.theme.name,
            }
        }
        if message.url is not None and len(message.url) > 0:
            request["data"]["uri"] = message.url

        connection.request('POST', '/1/push', json.dumps(request), {
               "X-Parse-Application-Id": "DUMkDMglUrCy4hmjQtMbMwGN9bwhM5avgW9FQOgW",
               "X-Parse-REST-API-Key": "um6O1RPz60XNlthGgtMRTOpA4C63kUuvJaCKxktO",
               "Content-Type": "application/json"
        })
        result = json.loads(connection.getresponse().read())
        return result

    def add_breadcrumbs(self, request, pk):
        theme = models.Theme.objects.get(pk=pk)
        request.breadcrumbs([
            ("Главная", reverse("main")),
            ("Личный кабинет", reverse("account", args=[request.user.id])),
            (u"Приложение '%s'"%theme.application.name, reverse("app_details", args=[theme.application.id])),
            (u"Рассылка '%s'"%theme.name, reverse("theme_details", args=[pk])),
        ])

    def get_messages_table(self, request, pk):
        messages_table = tables.MessagesTable(models.Message.objects.filter(theme=models.Theme.objects.get(pk=pk)))
        RequestConfig(request).configure(messages_table)
        return messages_table

    @method_decorator(login_required)
    def post(self, request, pk):
        self.add_breadcrumbs(request, pk)
        messages_table = self.get_messages_table(request, pk)
        message = models.Message(theme=models.Theme.objects.get(pk=pk), creation_date=timezone.now())
        create_message_form = forms.CreateMessageForm(request.POST, instance=message)
        if create_message_form.is_valid():
            message = create_message_form.save()
            self.send_message(message)
            return self.get(request, pk)
        return render(request, "notifications/theme_details.html",
            {
                "messages_table": messages_table,
                "create_message_form": create_message_form,
            })

    @method_decorator(login_required)
    def get(self, request, pk):
        self.add_breadcrumbs(request, pk)
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

    def response_by_filepath(self, path, filename = None):
        filename = filename if filename is not None else path.split('/')[-1]
        file = StringIO(open(path, "rb").read())
        mimetype = mimetypes.guess_type(os.path.basename(path))[0]
        response = HttpResponse(file, content_type='application/%s'%str(mimetype))
        response['Content-Disposition'] = 'attachment; filename="%s"'%filename
        return response

    def create_key(self, key, user, app_directory):
        key_path = os.path.join(app_directory, "app", "key.keystore")
        if (os.path.exists(key_path)):
            os.remove(key_path)
        if key.path is not None:
            shutil.copy(key.path, key_path)
        else:
            with open(os.path.join(app_directory, "USER_DATA.txt"), "w+") as f:
                f.write("\n".join([
                    key.keystore_password,
                    key.keystore_password,
                    user.get_full_name(),
                    key.org_unit,
                    key.org_name,
                    key.city,
                    key.province,
                    key.country_code,
                    "y",
                    key.key_password,
                    key.key_password,
                ]) + "\n")
            os.system("{0} {2} alias < {1}".format(
                os.path.join(app_directory, "create_keystore.sh"),
                os.path.join(app_directory, "USER_DATA.txt"),
                os.path.join(app_directory, "app", "key")
            ))
            key.path = os.path.join(BASE_DIR, "media", "app_keys", "key_%i.keystore"%key.id)
            if not os.path.exists(os.path.dirname(key.path)):
                os.makedirs(os.path.dirname(key.path))
            shutil.copy(key_path, key.path)
            key.save()

    def build_app(self, user, app):
        #Copy application
        template_directory = os.path.join(BASE_DIR, "SampleApplications", "NotificationApp")
        app_directory = os.path.join(BASE_DIR, "SampleApplications", "%i"%app.id)
        if (os.path.exists(app_directory)):
            shutil.rmtree(app_directory)
        shutil.copytree(template_directory, app_directory)

        #Insert image to application
        logging.info("Inserting image...")
        for root, dirs, files in os.walk(os.path.join(app_directory, "app/src/main/res/")):
            if "launch_image.png" in files:
                image_path = os.path.join(root, "launch_image.png")
                os.remove(image_path)
                shutil.copy(app.image.path, image_path)

        #Insert appID to application source code
        logging.info("Inserting application ID")
        for root, dirs, files in os.walk(os.path.join(app_directory, "app", "src")):
            if "ApplicationManager.java" in files:
                file_path = os.path.join(root, "ApplicationManager.java")
                with open(file_path) as f:
                    data = f.read()
                with open(file_path, "w") as f:
                    f.write(data.replace("SOME_HASH", "%i"%app.id))
                break

        if app.key is not None:
            self.create_key(app.key, user, app_directory)
            mode = "Release"
        else:
            mode = "Debug"

        logging.info("Building...")
        # build = pexpect.spawn(os.path.join(c + " assemble%s"%mode,
        #                       cwd=app_directory, env = {"JAVA_HOME": "/bin/java"})

        # build = pexpect.spawn("python",
        #                       [
        #                           os.path.join(app_directory, "build.py"),
        #                           os.path.join(app_directory, "gradlew"),
        #                           "Debug",
        #                           app_directory
        #                       ])
        # if mode == "Release":
        #     build.expect(".*Keystore password.*")
        #     build.sendline(app.key.keystore_password)
        #     build.expect(".*Key password.*")
        #     build.sendline(app.key.key_password)
        # build.expect(pexpect.EOF, timeout=120)
        #logging.info(str(build.before) + "\n" + str(build.after))

        out = pexpect.run("python " + " ".join([
                                os.path.join(app_directory, "build.py"),
                                os.path.join(app_directory, "gradlew"),
                                mode,
                                app_directory]),
                          cwd=app_directory,
                          events={
                              ".*Keystore password.*": app.key.keystore_password if app.key is not None else "",
                              ".*Key password.*": app.key.key_password if app.key is not None else ""
                          })
        logging.info(out)
        logging.info("Build finished!")
        return os.path.join(app_directory, "app", "build", "outputs", "apk", "app-%s.apk"%mode.lower())

    @method_decorator(login_required)
    def post(self, request, pk, hash):
        import shutil, hashlib
        path_to_apk = self.build_app(request.user, models.MobileApp.objects.get(pk=pk))
        hash = hashlib.md5(path_to_apk).hexdigest()
        if not os.path.exists(os.path.join(MEDIA_ROOT, "media/apps_to_download")):
            os.makedirs(os.path.join(MEDIA_ROOT, "media/apps_to_download"))
        shutil.move(path_to_apk, os.path.join(MEDIA_ROOT, "media/apps_to_download/%s"%hash))
        shutil.rmtree(os.path.join(BASE_DIR, "SampleApplications", pk))
        return hash

    @method_decorator(login_required)
    def get(self, request, pk, hash = None):
        if hash is not None:
            link = os.path.join(MEDIA_ROOT, "media/apps_to_download/%s"%hash)
            mode = "release" if models.MobileApp.objects.get(pk=pk).key is not None else "debug"
            return self.response_by_filepath(link, "application-{0}.apk".format(mode))
        return render(request, "notifications/download_app.html")
