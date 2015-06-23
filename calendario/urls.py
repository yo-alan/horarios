from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /calendario/
    url(r'^$', views.all, name='all'),
    # ex: /calendario/all/
    url(r'^all/$', views.all, name='all'),
    # ex: /calendario/profesional/all/
    url(r'^profesional/all/$', views.profesional_all, name='profesional_all'),
    # ex: /calendario/profesional/add/
    url(r'^profesional/add/$', views.profesional_add, name='profesional_add'),
    # ex: /calendario/profesional/edit/
    url(r'^profesional/edit/$', views.profesional_edit, name='profesional_edit'),
    # ex: /calendario/5/
    url(r'^(?P<calendario_id>[0-9]+)/$', views.detail, name='detail'),
]
