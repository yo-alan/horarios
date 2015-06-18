from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /calendario/all/
    url(r'^all/$', views.all, name='all'),
    # ex: /calendario/profesional/all/
    url(r'^profesional/all/$', views.profesional_all, name='profesional_all'),
    # ex: /calendario/5/
    url(r'^(?P<calendario_id>[0-9]+)/$', views.detail, name='detail'),
]
