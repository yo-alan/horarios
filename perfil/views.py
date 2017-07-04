# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.validators import validate_email
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.decorators import login_required

from calendario.models import Profesional

from .models import Persona
from .models import Actividad
from .models import Usuario
from .models import Institucion

PAGE_LENGTH = 10

@login_required(login_url='/index/')
def index(request):
    
    actividades = Actividad.objects.filter(usuario=request.user.username).order_by('-fecha')
    
    context = {"user": request.user, "actividades": actividades}
    
    return render(request, 'perfil/home.html', context)

@login_required(login_url='/index/')
def editar(request):
    
    if request.method != 'POST':
        return render(request, 'perfil/editar.html')
        
    try:
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Editaste los datos de tu perfil."
        
        actividad.save()
        
        data = {'mensaje': "Los datos se actualizaron exitosamente."}
        
    except:
        
        data = {'error': "No se pudo editar el perfil."}
    
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def administracion(request):
    return render(request, 'perfil/administracion.html')

@login_required(login_url='/index/')
def user_all(request, pagina=1):
    
    if not request.user.has_perm('auth.puede_ver_usuario'):
        return render(request, 'calendario/denied.html')
    
    instituciones = request.user.usuario.instituciones.all()
    
    total_usuarios = Usuario.objects.filter(instituciones=instituciones).order_by('persona__apellido', 'persona__nombre')
    
    total_usuarios = list(total_usuarios)
    
    for usuario in total_usuarios[:]:
        if usuario == request.user.usuario:
            total_usuarios.remove(usuario)
    
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
    
    if not request.user.has_perm('auth.puede_agregar_usuario'):
        return render(request, 'calendario/denied.html')
    
    if request.method != 'POST':
        return render(request, 'perfil/user/add.html')
    
    try:
        
        transaction.set_autocommit(False)
        
        institucion = request.user.usuario.instituciones.all()[0]
        
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        tipo = request.POST['tipo']
        
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        fecha_nacimiento = request.POST['fecha_nacimiento']
        cuil = request.POST['cuil']
        genero = request.POST['genero']
        
        if len(username) < 4:
            raise Exception("El nombre de usuario debe contener 4 o más caracteres.")
        
        validate_email(email)
        
        if len(password) < 6:
            raise Exception("El contraseña debe contener 6 o más caracteres.")
        
        user = User()
        
        user.username = username
        user.set_password(password)
        user.email = email
        user.first_name = nombre
        user.last_name = apellido
        
        user.save()
        
        usuario = Usuario()
        
        usuario.user = user
        
        if tipo == 'profesional':
            
            profesional = Profesional()
            
            profesional.set_nombre(nombre)
            profesional.set_apellido(apellido)
            profesional.set_fecha_nacimiento(fecha_nacimiento)
            profesional.set_cuil(cuil)
            profesional.set_genero(genero)
            
            profesional.save()
            
            usuario.persona = profesional
            
            group = Group.objects.get(name='Profesionales')
            
        else:
            
            persona = Persona()
            
            persona.set_nombre(nombre)
            persona.set_apellido(apellido)
            persona.set_fecha_nacimiento(fecha_nacimiento)
            persona.set_cuil(cuil)
            persona.set_genero(genero)
            
            persona.save()
            
            usuario.persona = persona
            
            if tipo == 'directivo':
                group = Group.objects.get(name='Directivos')
            else:
                group = Group.objects.get(name='Administradores')
        
        usuario.save()
        
        usuario.instituciones.add(institucion)
        
        usuario.save()
        
        group.user_set.add(user)
        
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
            
        elif 'cuil' in data['error']:
            data['campo'] = 'cuil'
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def user_detail(request, user_id):
    
    if not request.user.has_perm('auth.puede_editar_usuario'):
        return render(request, 'calendario/denied.html')
    
    usuario = get_object_or_404(Usuario, pk=user_id)
    
    context = {'usuario': usuario}
    
    return render(request, 'perfil/user/detail.html', context)

@login_required(login_url='/index/')
def user_edit(request):
    
    if not request.user.has_perm('auth.puede_editar_usuario'):
        return render(request, 'calendario/denied.html')
    
    try:
        
        transaction.set_autocommit(False)
        
        usuario_id = request.POST['usuario_id']
        
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        tipo = request.POST['tipo']
        
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        fecha_nacimiento = request.POST['fecha_nacimiento']
        cuil = request.POST['cuil']
        genero = request.POST['genero']
        
        if len(username) < 4:
            raise Exception("El nombre de usuario debe contener 4 o mas caracteres.")
        
        validate_email(email)
        
        if len(password) < 6:
            raise Exception("El contraseña debe contener 6 o más caracteres.")
        
        usuario = Usuario.objects.get(id=usuario_id)
        
        usuario.user.username = username
        
        if password != '******':
            usuario.user.set_password(password)
        
        usuario.user.email = email
        usuario.user.first_name = nombre
        usuario.user.last_name = apellido
        
        try:
            usuario.persona = Profesional.create(usuario.persona.id)
        except Exception as ex:
            pass

        try:
            # Unica vista en donde tipo esta capitalizado y en plural.
            group_name = usuario.user.groups.all()[0].name
            
            group = Group.objects.get(name=group_name)
        except:
            raise Exception("El tipo de usuario no es válido.")

        group.user_set.remove(usuario.user)
        
        nuevo_group = group = Group.objects.get(name=tipo)
        
        nuevo_group.user_set.add(usuario.user)
        
        if group.name != 'Profesionales' and tipo == 'Profesionales':
            
            usuario.persona.delete()
            
            persona = Profesional()
            
        elif group.name == 'Profesionales' and tipo != 'Profesionales':
            
            usuario.persona.delete()
            
            persona = Persona()
        else:
            persona = usuario.persona
        
        persona.set_nombre(nombre)
        persona.set_apellido(apellido)
        persona.set_fecha_nacimiento(fecha_nacimiento)
        persona.set_cuil(cuil)
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
            
        elif 'cuil' in data['error']:
            data['campo'] = 'cuil'
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def user_diactivate(request):
    
    if not request.user.has_perm('auth.puede_editar_usuario'):
        return render(request, 'calendario/denied.html')
    
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
    
    if not request.user.has_perm('auth.puede_editar_usuario'):
        return render(request, 'calendario/denied.html')
    
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
    
    if not request.user.has_perm('auth.puede_ver_institucion'):
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
    
    if not request.user.has_perm('auth.puede_agregar_institucion'):
        return render(request, 'calendario/denied.html')
    
    if request.method != 'POST':
        return render(request, 'perfil/institucion/add.html')
    
    try:
        
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        tipo = request.POST['tipo']
        documento = request.POST['documento']
        verificador = request.POST['verificador']
        
        institucion = Institucion()
        
        institucion.set_nombre(nombre)
        institucion.set_direccion(direccion)
        institucion.set_cuil(tipo + '-' + documento + '-' + verificador)
        
        institucion.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Agregaste la institucion " + str(institucion)
        
        actividad.save()
        
        data = {'mensaje': "La institucion se guardo existosamente."}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'nombre' in data['error']:
            data['campo'] = 'nombre'
        elif 'dirección'.decode('utf-8') in data['error']:
            data['campo'] = 'direccion'
        elif 'cuil' in data['error']:
            data['campo'] = 'cuil'
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def institucion_detail(request, institucion_id):
    
    if not request.user.has_perm('auth.puede_editar_institucion'):
        return render(request, 'calendario/denied.html')
    
    institucion = get_object_or_404(Institucion, pk=institucion_id)
    
    institucion.tipo = institucion.cuil.split('-')[0]
    institucion.documento = institucion.cuil.split('-')[1]
    institucion.verificador = institucion.cuil.split('-')[2]
    
    context = {'institucion': institucion}
    
    return render(request, 'perfil/institucion/detail.html', context)

@login_required(login_url='/index/')
def institucion_edit(request):
    
    if not request.user.has_perm('auth.puede_editar_institucion'):
        return render(request, 'calendario/denied.html')
    
    try:
    
        institucion_id = request.POST['institucion_id']
        
        institucion = get_object_or_404(Institucion, pk=institucion_id)
        
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        tipo = request.POST['tipo']
        documento = request.POST['documento']
        verificador = request.POST['verificador']
        
        institucion.set_nombre(nombre)
        institucion.set_direccion(direccion)
        institucion.set_cuil(tipo + '-' + documento + '-' + verificador)
        
        institucion.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Modificaste la institucion " + str(institucion)
        
        actividad.save()
        
        data = {'mensaje': "La institución fue modificada existosamente."}
    
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'nombre' in data['error']:
            data['campo'] = 'nombre'
        elif 'dirección'.decode('utf-8') in data['error']:
            data['campo'] = 'direccion'
        elif 'cuil' in data['error']:
            data['campo'] = 'cuil'

    return JsonResponse(data)

@login_required(login_url='/index/')
def institucion_delete(request):
    
    if not request.user.has_perm('auth.puede_eliminar_institucion'):
        return render(request, 'calendario/denied.html')
    
    try:
    
        institucion_id = request.POST['institucion_id']
        
        institucion = get_object_or_404(Institucion, pk=institucion_id)
        
        institucion.delete()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Modificaste la institucion " + str(institucion)
        
        actividad.save()
        
        data = {'mensaje': "La institución fue modificada existosamente."}
    
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'nombre' in data['error']:
            data['campo'] = 'nombre'
        elif 'dirección'.decode('utf-8') in data['error']:
            data['campo'] = 'direccion'

    return JsonResponse(data)
