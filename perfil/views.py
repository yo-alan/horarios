# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.db import transaction
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User, Permission

from calendario.models import Profesional

from .models import Actividad
from .models import Usuario_profesional, Usuario_directivo

PAGE_LENGTH = 10

def index(request):
    
    if not request.user.is_authenticated():
        return render(request, 'calendario/index.html')
    
    if request.user.has_perm('auth.profesional'):
        print "Not so super"
    
    actividades = Actividad.objects.filter(usuario=request.user.username)
    
    context = {"user": request.user, "actividades": actividades}
    
    return render(request, 'perfil/home.html', context)
    
def editar(request):
    
    context = {}
    
    return render(request, 'perfil/editar.html', context)

def administracion(request):
    
    context = {}
    
    return render(request, 'perfil/administracion.html', context)

def user_all(request, pagina=1):
    
    if request.user.has_perm('auth.administrador'):
        return render(request, 'calendario/denied.html')
    
    total_users = User.objects.filter(is_active=True).order_by('username')

    paginator = Paginator(total_users, PAGE_LENGTH)

    try:
        users = paginator.page(pagina)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    context = {'users': users}
    
    return render(request, 'perfil/user/all.html', context)

def user_add(request):
    
    if request.method != 'POST':
        return render(request, 'perfil/user/add.html')
    
    data = {}
    
    try:
        
        transaction.set_autocommit(False)
        
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        tipo = request.POST['tipo']
        
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        cuil = '23-38046045-9'
        fecha_nacimiento = request.POST['fecha_nacimiento']
        genero = request.POST['genero']
        
        user = User()
        
        user.username = username
        user.set_password(password)
        user.email = email
        user.first_name = nombre
        user.last_name = apellido
        
        user.save()
        
        if tipo == 'profesional':
            
            profesional = Profesional()
            
            profesional.nombre = nombre
            profesional.apellido = apellido
            profesional.cuil = cuil
            
            profesional.save()
            
            usuario_profesional = Usuario_profesional()
            
            usuario_profesional.user = user
            usuario_profesional.profesional = profesional
            usuario_profesional.genero = genero
            
            usuario_profesional.save()
            
            permission = Permission.objects.get(codename='profesional')
            
            user.user_permissions.add(permission)
            
            user.save()
            
        else:
            
            usuario_directivo = Usuario_directivo()
            
            usuario_directivo.user = user
            usuario_directivo.genero = genero
            
            usuario_directivo.save()
            
            permission = Permission.objects.get(codename='directivo')
            
            user.user_permissions.add(permission)
            
            user.save()

        print username
        print password
        print email
        print tipo
        
        print nombre
        print apellido
        print fecha_nacimiento
        print genero
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Agregaste al usuario " + username
        
        actividad.save()
        
        transaction.commit()
        
        data  = {'mensaje': "El usuario fue creado exitosamente."}
        
    except Exception as ex:
        
        transaction.rollback()
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'username' in data['error']:
            
            exists = "duplicate key value violates unique constraint"
            
            if exists in data['error']:
                data['error'] = "Ya existe el nombre de usuario."
            
            data['campo'] = 'username'
    
    return JsonResponse(data)

def user_detail(request, user_id):
    
    context = {}
    
    return render(request, 'perfil/user/detail.html', context)

def user_edit(request, user_id):
    
    context = {}
    
    return render(request, 'perfil/user/detail.html', context)

def user_delete(request):
    
    if request.user.has_perm('auth.administrador'):
        return render(request, 'calendario/denied.html')
    
    data = {}
    
    try:
        
        user_id = request.POST['user_id']
        
        user = User.objects.get(id=user_id)
        
        try:
            usuario = Usuario_profesional.get(user=user)
        except:
            usuario = Usuario_directivo.get(user=user)
        
        usuario.is_active = False
        
        usuario.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Eliminaste el usuario " + user.username
        
        actividad.save()
        
        data = {'mensaje': "El usuario fue eliminado exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)
