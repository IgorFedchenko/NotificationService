# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import notifications.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias_name', models.CharField(max_length=20)),
                ('key_password', models.CharField(max_length=30)),
                ('full_name', models.CharField(max_length=40)),
                ('org_unit', models.CharField(max_length=40)),
                ('org_name', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=40)),
                ('province', models.CharField(max_length=40)),
                ('country_code', models.CharField(max_length=40, choices=[(b'RU', b'RU')])),
                ('alias_password', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.CharField(max_length=1000)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MobileApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300)),
                ('image', models.FileField(upload_to=notifications.models.get_mobile_app_data_path)),
                ('key', models.ForeignKey(related_name='applications', to='notifications.AppKey', null=True)),
                ('user', models.ForeignKey(related_name='applications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('application', models.ForeignKey(related_name='themes', to='notifications.MobileApp')),
                ('user', models.ForeignKey(related_name='themes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='theme',
            field=models.ForeignKey(related_name='messages', to='notifications.Theme'),
            preserve_default=True,
        ),
    ]
