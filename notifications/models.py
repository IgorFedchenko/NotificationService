from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from hashlib import md5


def get_mobile_app_data_path(instance, filename):
    dt = timezone.now()
    return u'media/apps_data/{0}/{1}/{2}/{3}'.format(dt.year, dt.month, dt.day, md5(filename).digest())

class AppKey(models.Model):
    alias_name = models.CharField(max_length=20)
    key_password = models.CharField(max_length=30)
    full_name = models.CharField(max_length=40)
    org_unit = models.CharField(max_length=40)
    org_name = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    province = models.CharField(max_length=40)
    country_code = models.CharField(max_length=40, choices=[("RU","RU")])
    alias_password = models.CharField(max_length=30)

class MobileApp(models.Model):
    user = models.ForeignKey(User, related_name="applications")
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to=get_mobile_app_data_path)
    key = models.ForeignKey(AppKey, related_name="applications")

    def __unicode__(self):
        return self.name

class Theme(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name="themes")
    apps = models.ManyToManyField(MobileApp, related_name="themes")

    def __unicode__(self):
        return self.name

class Message(models.Model):
    theme = models.ForeignKey(Theme, related_name="messages")
    data = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now=True)
