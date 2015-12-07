# -*- coding: utf-8 -*-
from django.shortcuts import render

def index(request):
    
    if not request.user.is_authenticated():
        return render(request, 'calendario/index.html')
    
    context = {"user": request.user}
    
    return render(request, 'perfil/home.html', context)
    
