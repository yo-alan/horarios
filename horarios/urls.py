"""horarios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from calendario import views as calendario_views
from perfil import views as perfil_views

urlpatterns = [
    url(r'^$', calendario_views.index, name='index'),
    url(r'^index/$', calendario_views.index, name='index'),
    url(r'^log_in/$', calendario_views.log_in, name='log_in'),
    url(r'^log_out/$', calendario_views.log_out, name='log_out'),
    url(r'^calendario/', include('calendario.urls', namespace="calendario")),
    url(r'^perfil/', include('perfil.urls', namespace="perfil")),
    url(r'^admin/', include(admin.site.urls)),
]

handler400 = calendario_views.bad_request
handler403 = calendario_views.permission_denied
handler404 = calendario_views.page_not_found
handler500 = calendario_views.server_error
