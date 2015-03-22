from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from hashlib import md5


def get_mobile_app_data_path(instance, filename):
    dt = timezone.now()
    return u'media/apps_data/{0}/{1}/{2}/{3}'.format(dt.year, dt.month, dt.day, md5(filename).digest())

class MobileApp(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to=get_mobile_app_data_path)

    def __unicode__(self):
        return self.name

class Theme(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    apps = models.ManyToManyField(MobileApp)

    def __unicode__(self):
        return self.name

class Message(models.Model):
    theme = models.ForeignKey(Theme)
    data = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now=True)
