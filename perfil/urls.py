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
    url(r'^user/edit/(?P<user_id>[0-9]+)/$', views.user_edit, name='user_edit'),
    url(r'^user/delete/$', views.user_delete, name='user_delete'),
]
