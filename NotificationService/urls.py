from django.conf.urls import patterns, include, url
from django.contrib import admin

from notifications import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.Main.as_view(), name='main'),
    url(r'^registration/$', views.Registration.as_view(), name='registration'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^account/(?P<pk>\d+)$', views.Account.as_view(), name='account'),
    url(r'^create_app/$', views.CreateApplication.as_view(), name='create_app'),
    url(r'^app_keys_manage/$', views.ApplicationKeysManage.as_view(), name='app_keys_manage'),
    url(r'^app_details/(?P<pk>\d+)$', views.ApplicationDetails.as_view(), name='app_details'),
    url(r'^theme_details/(?P<pk>\d+)$', views.ThemeDetails.as_view(), name='theme_details'),
    url(r'^message_details/(?P<pk>\d+)$', views.MessageDetails.as_view(), name='message_details'),
    url(r'^delete_app/(?P<pk>\d+)$', views.delete_app, name='delete_app'),
    url(r'^delete_theme/(?P<pk>\d+)$', views.delete_theme, name='delete_theme'),
    url(r'^delete_app_key/(?P<pk>\d+)$', views.delete_app_key, name='delete_app_key'),
    url(r'^download_app/(?P<pk>\d+)(/(?P<hash>[\da-z]+))?$',views.DownloadApplication.as_view(), name="download_app"),
)
