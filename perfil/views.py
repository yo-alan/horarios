# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.validators import validate_email
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required

from calendario.models import Persona, Profesional

from .models import Actividad
from .models import Usuario
from .models import Institucion

PAGE_LENGTH = 10

@login_required(login_url='/index/')
def index(request):
    
    actividades = Actividad.objects.filter(usuario=request.user.username)
    
    context = {"user": request.user, "actividades": actividades}
    
    return render(request, 'perfil/home.html', context)

@login_required(login_url='/index/')
def editar(request):
    
    context = {}
    
    return render(request, 'perfil/editar.html', context)

@login_required(login_url='/index/')
def administracion(request):
    
    context = {}
    
    return render(request, 'perfil/administracion.html', context)

@login_required(login_url='/index/')
def user_all(request, pagina=1):
    
    if request.user.has_perm('auth.administrador'):
        return render(request, 'calendario/denied.html')
    
    total_usuarios = Usuario.objects.all()
    
    for usuario in total_usuarios[:]:
        
        if isinstance(usuario.persona, Profesional):
            usuario.persona._profesional = True

    paginator = Paginator(total_usuarios, PAGE_LENGTH)

    try:
        usuarios = paginator.page(pagina)
    except PageNotAnInteger:
        usuarios = paginator.page(1)
    except EmptyPage:
        usuarios = paginator.page(paginator.num_pages)
    
    context = {'usuarios': usuarios}
    
    return render(request, 'perfil/user/all.html', context)

@login_required(login_url='/index/')
def user_add(request):
    
    if request.user.has_perm('auth.administrador'):
        return render(request, 'calendario/denied.html')
    
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
        
        if len(username) < 4:
            raise Exception("El nombre de usuario debe contener 4 o mas caracteres.")
        
        validate_email(email)
        
        if len(password) < 6:
            raise Exception("El contraseña debe contener 6 o más caracteres.")
        
        if fecha_nacimiento == '':
            raise Exception("La fecha de nacimiento no es válida.")
        
        fecha_nacimiento = datetime.datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
        
        user = User()
        
        user.username = username
        user.set_password(password)
        user.email = email
        user.first_name = nombre
        user.last_name = apellido
        
        user.save()
        
        if tipo == 'profesional':
            
            profesional = Profesional()
            
            profesional.set_nombre(nombre)
            profesional.set_apellido(apellido)
            profesional.set_cuil(cuil)
            profesional.set_fecha_nacimiento(fecha_nacimiento)
            profesional.set_genero(genero)
            
            profesional.save()
            
            usuario = Usuario()
            
            usuario.user = user
            usuario.persona = profesional
            
            usuario.save()
            
            permission = Permission.objects.get(codename='profesional')
            
        else:
            
            persona = Persona()
            
            persona.set_nombre(nombre)
            persona.set_apellido(apellido)
            persona.set_cuil(cuil)
            persona.set_fecha_nacimiento(fecha_nacimiento)
            persona.set_genero(genero)
            
            persona.save()
            
            usuario = Usuario()
            
            usuario.user = user
            usuario.persona = persona
            
            usuario.save()
            
            permission = Permission.objects.get(codename='directivo')
        
        user.user_permissions.add(permission)
        
        user.save()

        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Agregaste al usuario " + username
        
        actividad.save()
        
        transaction.commit()
        
        data  = {'mensaje': "El usuario fue creado exitosamente."}
        
    except Exception as ex:
        
        transaction.rollback()
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'username' in data['error'] or "nombre de usuario" in data['error']:
            
            exists = "duplicate key value violates unique constraint"
            
            if exists in data['error']:
                data['error'] = "Ya existe el nombre de usuario."
            
            data['campo'] = 'username'
            
        elif 'email' in data['error']:
            
            data['error'] = 'La dirección de email no es válida.'
            
            data['campo'] = 'email'
            
        elif 'contraseña'.decode('utf-8') in data['error']:
            
            data['campo'] = 'password'
            
        elif 'nombre' in data['error']:
            data['campo'] = 'nombre'
            
        elif 'apellido' in data['error']:
            data['campo'] = 'apellido'
            
        elif 'nacimiento' in data['error']:
            data['campo'] = 'fecha_nacimiento'
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def user_detail(request, user_id):
    
    if request.user.has_perm('auth.administrador'):
        return render(request, 'calendario/denied.html')
    
    usuario = get_object_or_404(Usuario, pk=user_id)
    
    usuario = Usuario.objects.get(id=user_id)
    
    if isinstance(usuario.persona, Profesional):
        usuario.persona._profesional = True
    
    context = {'usuario': usuario}
    
    return render(request, 'perfil/user/detail.html', context)

@login_required(login_url='/index/')
def user_edit(request):
    
    if request.user.has_perm('auth.administrador'):
        return render(request, 'calendario/denied.html')
    
    data = {}
    
    try:
        
        transaction.set_autocommit(False)
        
        usuario_id = request.POST['usuario_id']
        
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        tipo = request.POST['tipo']
        
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        cuil = '23-38046045-9'
        fecha_nacimiento = request.POST['fecha_nacimiento']
        genero = request.POST['genero']
        
        if len(username) < 4:
            raise Exception("El nombre de usuario debe contener 4 o mas caracteres.")
        
        validate_email(email)
        
        if len(password) < 6:
            raise Exception("El contraseña debe contener 6 o más caracteres.")
        
        if fecha_nacimiento == '':
            raise Exception("La fecha de nacimiento no es válida.")
        
        fecha_nacimiento = datetime.datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
        
        usuario = Usuario.objects.get(id=usuario_id)
        
        usuario.user.username = username
        usuario.user.set_password(password)
        usuario.user.email = email
        usuario.user.first_name = nombre
        usuario.user.last_name = apellido
        
        try:
            usuario.persona = Profesional.create(usuario.persona.id)
        except Exception as ex:
            pass
        
        if isinstance(usuario.persona, Profesional) and tipo == 'directivo':
            
            usuario.persona.delete()
            
            permission = Permission.objects.get(codename='profesional')
            
            usuario.user.user_permissions.remove(permission)
            
            permission = Permission.objects.get(codename='directivo')
            
            usuario.user.user_permissions.add(permission)
            
            persona = Persona()
            
        elif not isinstance(usuario.persona, Profesional) and tipo == 'profesional':
            
            usuario.persona.delete()
            
            permission = Permission.objects.get(codename='directivo')
            
            usuario.user.user_permissions.remove(permission)
            
            permission = Permission.objects.get(codename='profesional')
            
            usuario.user.user_permissions.add(permission)
            
            persona = Profesional()
        else:
            persona = usuario.persona
        
        persona.set_nombre(nombre)
        persona.set_apellido(apellido)
        persona.set_cuil(cuil)
        persona.set_fecha_nacimiento(fecha_nacimiento)
        persona.set_genero(genero)
        
        persona.save()
        
        usuario.persona = persona
        
        usuario.user.save()
        
        usuario.save()

        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Modificaste al usuario " + username
        
        actividad.save()
        
        transaction.commit()
        
        data  = {'mensaje': "El usuario fue modificado exitosamente."}
        
    except Exception as ex:
        
        transaction.rollback()
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'username' in data['error'] or "nombre de usuario" in data['error']:
            
            exists = "duplicate key value violates unique constraint"
            
            if exists in data['error']:
                data['error'] = "Ya existe el nombre de usuario."
            
            data['campo'] = 'username'
            
        elif 'email' in data['error']:
            
            data['error'] = 'La dirección de email no es válida.'
            
            data['campo'] = 'email'
            
        elif 'contraseña'.decode('utf-8') in data['error']:
            data['campo'] = 'password'
            
        elif 'nombre' in data['error']:
            data['campo'] = 'nombre'
            
        elif 'apellido' in data['error']:
            data['campo'] = 'apellido'
            
        elif 'nacimiento' in data['error']:
            data['campo'] = 'fecha_nacimiento'
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def user_diactivate(request):
    
    if request.user.has_perm('auth.administrador'):
        return render(request, 'calendario/denied.html')
    
    data = {}
    
    try:

        usuario_id = request.POST['user_id']
        
        usuario = Usuario.objects.get(id=usuario_id)
        
        usuario.user.is_active = False
        
        usuario.user.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Desactivaste al usuario " + user.username
        
        actividad.save()
        
        data = {'mensaje': "El usuario fue desactivado exitosamente."}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def user_activate(request):
    
    if request.user.has_perm('auth.administrador'):
        return render(request, 'calendario/denied.html')
    
    data = {}
    
    try:

        usuario_id = request.POST['user_id']
        
        usuario = Usuario.objects.get(id=usuario_id)
        
        usuario.user.is_active = True
        
        usuario.user.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Activaste al usuario " + user.username
        
        actividad.save()
        
        data = {'mensaje': "El usuario fue activado exitosamente."}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def institucion_all(request, pagina=1):
    
    if request.user.has_perm('auth.administrador'):
        return render(request, 'calendario/denied.html')
    
    total_instituciones = Institucion.objects.all()

    paginator = Paginator(total_instituciones, PAGE_LENGTH)

    try:
        instituciones = paginator.page(pagina)
    except PageNotAnInteger:
        instituciones = paginator.page(1)
    except EmptyPage:
        instituciones = paginator.page(paginator.num_pages)
    
    context = {'instituciones': instituciones}
    
    return render(request, 'perfil/institucion/all.html', context)

@login_required(login_url='/index/')
def institucion_add(request):
    
    if request.method != 'POST':
        return render(request, 'perfil/institucion/add.html')
    
    data = {}
    
    try:
        
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        
        if nombre == '':
            raise Exception("El nombre no puede estar vacío.")
        
        if direccion == '':
            raise Exception("La dirección no puede estar vacía.")
        
        institucion = Institucion()
        
        institucion.nombre = nombre
        institucion.direccion = direccion
        
        institucion.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Agregaste la institucion " + str(institucion)
        
        actividad.save()
        
        data['mensaje'] = "La institucion se guardo existosamente."
        
    except Exception as ex:
        
        data['error'] = str(ex).decode('utf-8')
        
        if 'nombre' in data['error']:
            data['campo'] = 'nombre'
        elif 'dirección'.decode('utf-8') in data['error']:
            data['campo'] = 'direccion'
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def institucion_detail(request, institucion_id):
    
    institucion = get_object_or_404(Institucion, pk=institucion_id)
    
    context = {'institucion': institucion}
    
    return render(request, 'perfil/institucion/detail.html', context)

@login_required(login_url='/index/')
def institucion_edit(request):
    
    if request.user.has_perm('auth.administrador'):
        return render(request, 'calendario/denied.html')
    
    try:
        
        institucion_id = request.POST['institucion_id']
        
        institucion = get_object_or_404(Institucion, pk=institucion_id)
        
        institucion.nombre = nombre
        institucion.direccion = direccion
        
        institucion.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Modificaste la institucion " + str(institucion)
        
        actividad.save()
        
        data['mensaje'] = "La institución fue modificada existosamente."
    
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        data['error'] = str(ex).decode('utf-8')
        
        if 'nombre' in data['error']:
            data['campo'] = 'nombre'
        elif 'dirección'.decode('utf-8') in data['error']:
            data['campo'] = 'direccion'

    return JsonResponse(data)

@login_required(login_url='/index/')
def institucion_delete(request):
    
    data = {}
    
    return JsonResponse(data)
