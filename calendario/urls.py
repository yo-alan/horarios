from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /calendario/5/
    url(r'^(?P<calendario_id>[0-9]+)/$', views.detail, name='detail'),
]
