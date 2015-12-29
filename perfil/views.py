# -*- coding: utf-8 -*-
from django.shortcuts import render

from .models import Actividad

def index(request):
    
    if not request.user.is_authenticated():
        return render(request, 'calendario/index.html')
    
    actividades = Actividad.objects.filter(usuario=request.user.username)
    
    context = {"user": request.user, "actividades": actividades}
    
    return render(request, 'perfil/home.html', context)
    
