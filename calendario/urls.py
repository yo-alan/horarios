from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /calendario/
    url(r'^$', views.all, name='all'),
    # ex: /calendario/all/
    url(r'^all/$', views.all, name='all'),
    # ex: /calendario/add/5
    url(r'^add/(?P<espacio_id>[0-9]+)/$', views.add, name='add'),
    # ex: /calendario/5/
    url(r'^(?P<calendario_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /calendario/generar/
    url(r'^generar/$', views.generar, name='generar'),
    
    # ex: /calendario/acerca
    url(r'^acerca/$', views.acerca, name='acerca'),
    
    # ex: /calendario/espacio/
    url(r'^espacio/$', views.espacio_all, name='espacio_all'),
    # ex: /calendario/espacio/all/
    url(r'^espacio/all/$', views.espacio_all, name='espacio_all'),
    # ex: /calendario/espacio/5/
    url(r'^espacio/(?P<espacio_id>[0-9]+)/$', views.espacio_detail, name='espacio_detail'),
    # ex: /calendario/espacio/all/pagina/
    url(r'^espacio/all/pagina/(?P<pagina>[0-9]+)/$', views.espacio_all, name='espacio_all'),
    # ex: /calendario/espacio/add/
    url(r'^espacio/add/$', views.espacio_add, name='espacio_add'),
    # ex: /calendario/espacio/edit/
    url(r'^espacio/edit/$', views.espacio_edit, name='espacio_edit'),
    # ex: /calendario/espacio/delete/
    url(r'^espacio/delete/$', views.espacio_delete, name='espacio_delete'),
    # ex: /calendario/espacio/horas/5
    url(r'^espacio/horas/(?P<espacio_id>[0-9]+)/$', views.espacio_horas, name='espacio_horas'),
    # ex: /calendario/espacio/especialidades/5
    url(r'^espacio/especialidades/(?P<espacio_id>[0-9]+)/$', views.espacio_add_especialidades, name='espacio_add_especialidades'),
    # ex: /calendario/espacio/profesionales/5
    url(r'^espacio/profesionales/(?P<espacio_id>[0-9]+)/$', views.espacio_add_profesionales, name='espacio_add_profesionales'),
    # ex: /calendario/espacio/horas/add/
    url(r'^espacio/horas/add/$', views.espacio_add_hora, name='espacio_add_hora'),
    
    # ex: /calendario/profesional/
    url(r'^profesional/$', views.profesional_all, name='profesional_all'),
    # ex: /calendario/profesional/all/
    url(r'^profesional/all/$', views.profesional_all, name='profesional_all'),
    # ex: /calendario/profesional/all/pagina/
    url(r'^profesional/all/pagina/(?P<pagina>[0-9]+)/$', views.profesional_all, name='profesional_all'),
    # ex: /calendario/profesional/add/
    url(r'^profesional/add/$', views.profesional_add, name='profesional_add'),
    # ex: /calendario/profesional/5
    url(r'^profesional/(?P<profesional_id>[0-9]+)/$', views.profesional_detail, name='profesional_detail'),
    # ex: /calendario/profesional/edit/
    url(r'^profesional/edit/$', views.profesional_edit, name='profesional_edit'),
    # ex: /calendario/profesional/delete/
    url(r'^profesional/delete/$', views.profesional_delete, name='profesional_delete'),
    # ex: /calendario/profesional/profesional_add_especialidades/
    url(r'^profesional/profesional_add_especialidades/$', views.profesional_add_especialidades, name='profesional_add_especialidades'),
    # ex: /calendario/profesional/profesional_add_restriccion/
    url(r'^profesional/profesional_add_restriccion/$', views.profesional_add_restriccion, name='profesional_add_restriccion'),
    
    # ex: /calendario/especialidad/
    url(r'^especialidad/$', views.especialidad_all, name='especialidad_all'),
    # ex: /calendario/especialidad/all/
    url(r'^especialidad/all/$', views.especialidad_all, name='especialidad_all'),
    # ex: /calendario/especialidad/all/pagina/
    url(r'^especialidad/all/pagina/(?P<pagina>[0-9]+)/$', views.especialidad_all, name='especialidad_all'),
    # ex: /calendario/especialidad/add/
    url(r'^especialidad/add/$', views.especialidad_add, name='especialidad_add'),
    # ex: /calendario/especialidad/5
    url(r'^especialidad/(?P<especialidad_id>[0-9]+)/$', views.especialidad_detail, name='especialidad_detail'),
    # ex: /calendario/especialidad/edit/
    url(r'^especialidad/edit/$', views.especialidad_edit, name='especialidad_edit'),
    # ex: /calendario/especialidad/delete/
    url(r'^especialidad/delete/$', views.especialidad_delete, name='especialidad_delete'),
    
    # ex: /calendario/restriccion/add/
    url(r'^restriccion/add/$', views.restriccion_add, name='restriccion_add'),
    # ex: /calendario/restriccion/edit/
    url(r'^restriccion/edit/$', views.restriccion_edit, name='restriccion_edit'),
    # ex: /calendario/restriccion/delete/
    url(r'^restriccion/delete/$', views.restriccion_delete, name='restriccion_delete'),
    # ex: /calendario/restriccion/getrestriccionesof/
    url(r'^restriccion/getrestriccionesof/$', views.getrestriccionesof, name='getrestriccionesof'),
]
