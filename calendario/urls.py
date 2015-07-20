from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /calendario/
    url(r'^$', views.all, name='all'),
    # ex: /calendario/all/
    url(r'^all/$', views.all, name='all'),
    # ex: /calendario/add/
    url(r'^add/$', views.add, name='add'),
    # ex: /calendario/5/
    url(r'^(?P<calendario_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /calendario/generar/
    url(r'^generar/$', views.generar, name='generar'),
    # ex: /calendario/profesional/
    url(r'^profesional/$', views.profesional_all, name='profesional_all'),
    # ex: /calendario/profesional/all/
    url(r'^profesional/all/$', views.profesional_all, name='profesional_all'),
    # ex: /calendario/profesional/add/
    url(r'^profesional/add/$', views.profesional_add, name='profesional_add'),
    # ex: /calendario/profesional/edit/
    url(r'^profesional/edit/(?P<profesional_id>[0-9]+)/$', views.profesional_edit, name='profesional_edit'),
    # ex: /calendario/profesional/delete/
    url(r'^profesional/delete/(?P<profesional_id>[0-9]+)/$', views.profesional_delete, name='profesional_delete'),
    # ex: /calendario/especialidad/
    url(r'^especialidad/$', views.especialidad_all, name='especialidad_all'),
    # ex: /calendario/especialidad/all/
    url(r'^especialidad/all/$', views.especialidad_all, name='especialidad_all'),
    # ex: /calendario/especialidad/add/
    url(r'^especialidad/add/$', views.especialidad_add, name='especialidad_add'),
    # ex: /calendario/especialidad/edit/
    url(r'^especialidad/edit/(?P<especialidad_id>[0-9]+)/$', views.especialidad_edit, name='especialidad_edit'),
    # ex: /calendario/especialidad/delete/
    url(r'^especialidad/delete/(?P<especialidad_id>[0-9]+)/$', views.especialidad_delete, name='especialidad_delete'),
]
