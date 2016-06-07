# -*- coding: utf-8 -*-
from django.shortcuts import render

from .models import Actividad

def index(request):
    
    if not request.user.is_authenticated():
        return render(request, 'calendario/index.html')
    
    if request.user.has_perm('auth.profesional'):
        print "Not so super"
    
    actividades = Actividad.objects.filter(usuario=request.user.username)
    
    for actividad in actividades:
        print actividad.fecha
    
    context = {"user": request.user, "actividades": actividades}
    
    return render(request, 'perfil/home.html', context)
    
