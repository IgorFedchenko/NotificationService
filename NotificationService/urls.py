from django.conf.urls import patterns, include, url
from django.contrib import admin

from notifications import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'', views.main, name='main'),
    url(r'registration/', views.main, name='registration'),
    url(r'account/', views.account, name='account'),
    url(r'create_app/', views.create_app, name='create_app'),
    url(r'create_theme/', views.create_theme, name='create_theme'),
    url(r'create_app_key/', views.create_app_key, name='create_app_key'),
    url(r'app_details/(?P<pk>\d+)', views.app_details, name='app_details'),
    url(r'theme_details/(?P<pk>\d+)', views.theme_details, name='theme_details'),
    url(r'message_details/(?P<pk>\d+)', views.message_details, name='message_details'),
)
