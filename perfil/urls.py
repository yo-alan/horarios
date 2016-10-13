# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^editar/$', views.editar, name='editar'),
    url(r'^administracion/$', views.administracion, name='administracion'),
    
    #~ user
    url(r'^user/all/$', views.user_all, name='user_all'),
    url(r'^user/add/$', views.user_add, name='user_add'),
    url(r'^user/detail/(?P<user_id>[0-9]+)/$', views.user_detail, name='user_detail'),
    url(r'^user/edit/$', views.user_edit, name='user_edit'),
    url(r'^user/activate/$', views.user_activate, name='user_activate'),
    url(r'^user/diactivate/$', views.user_diactivate, name='user_diactivate'),
    
    #~ institucion
    url(r'^institucion/all/$', views.institucion_all, name='institucion_all'),
    url(r'^institucion/add/$', views.institucion_add, name='institucion_add'),
    url(r'^institucion/detail/(?P<institucion_id>[0-9]+)/$', views.institucion_detail, name='institucion_detail'),
    url(r'^institucion/edit/$', views.institucion_edit, name='institucion_edit'),
    url(r'^institucion/delete/$', views.institucion_delete, name='institucion_delete'),
]
