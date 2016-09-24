# -*- coding: utf-8 -*-
import sys
import time
from datetime import datetime, timedelta

import cStringIO as StringIO
from xhtml2pdf import pisa
from cgi import escape
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context
from django.db.models import Q

from .models import Calendario
from .models import Profesional
from .models import Horario
from .models import Restriccion
from .models import Especialidad
from .models import Espacio
from .models import Hora
from .models import Coordinador
from .models import DiaHabil
from perfil.models import Actividad

DIAS = {0: 'Domingo', 1: 'Lunes', 2: 'Martes', 3: 'Miércoles',
        4: 'Jueves', 5: 'Viernes', 6: 'Sábado', 7: "Todos los días"}

DENSIDAD = 1

PAGE_LENGTH = 10

def bad_request(request):
    
    response = render(request, 'errors/400.html')
    
    response.status_code = 400
    
    return response

def permission_denied(request):
    
    response = render(request, 'errors/403.html')
    
    response.status_code = 403
    
    return response

def page_not_found(request):
    
    response = render(request, 'errors/404.html')
    
    response.status_code = 404
    
    return response

def server_error(request):
    
    response = render(request, 'errors/500.html')
    
    response.status_code = 500
    
    return response

def index(request):
    
    if not request.user.is_authenticated():
        return render(request, 'calendario/index.html')
    
    especialidades = Especialidad.objects.filter(estado="ON")
    profesionales = Profesional.objects.filter(estado="ON")
    espacios = Espacio.objects.filter(~Q(estado=Espacio.OFF))
    calendarios = Calendario.objects.all()
    
    context = {"user": request.user, "especialidades": especialidades,
                "profesionales": profesionales, "espacios": espacios,
                "calendarios": calendarios}
    
    return render(request, 'calendario/home.html', context)

def acerca(request):
    
    return render(request, 'calendario/acerca.html')

def log_in(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('index'))
    
    username = request.POST['username']
    password = request.POST['password']
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
    
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/index/')
def log_out(request):
    
    logout(request)
    
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/index/')
def all(request, pagina=1):
    
    total_calendarios = Calendario.objects.all().order_by('estado')
    paginator = Paginator(total_calendarios, PAGE_LENGTH)
    
    try:
        calendarios = paginator.page(pagina)
    except PageNotAnInteger:
        calendarios = paginator.page(1)
    except EmptyPage:
        calendarios = paginator.page(paginator.num_pages)
    
    context = {'calendarios': calendarios}
    
    return render(request, 'calendario/all.html', context)

@login_required(login_url='/index/')
def add(request, espacio_id):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method == 'POST':
        
        calendario = Calendario.create()
        
        calendario.espacio = Espacio.create(espacio_id)
        
        # Dividimos por 3, esa es la cantidad de atributos.
        # Mas 1 por que el primero es el csrf.
        for i in range(1, len(request.POST)/3+1):
            
            coordinador_id = request.POST[str(i) + '[coordinador]']
            desde = request.POST[str(i) + '[desde]']
            
            coordinador = Coordinador.objects.get(pk=coordinador_id)
            hora = Hora.objects.filter(hora_desde=desde)
            hora = hora.filter(espacio=calendario.espacio.id)
            
            dia_semana = request.POST[str(i) + '[dia]']
            
            # Creamos un horario y los completamos.
            horario = Horario()
            
            horario.coordinador = coordinador
            horario.hora_desde = hora[0].hora_desde
            horario.hora_hasta = hora[0].hora_hasta
            horario.dia_semana = dia_semana
            
            calendario.agregar_horario(horario)
        
        calendario.full_save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Agregó un calendario a " + str(espacio)
        
        actividad.save()
        
        data = {'mensaje': "El calendario fue creado exitosamente."}
        
        return JsonResponse(data)
    
    espacio = Espacio.create(espacio_id)
    
    dias = []
    
    for dia in espacio.dias_habiles:
        dias.append(DIAS[dia.dia])
    
    context = {'espacio': espacio, 'dias': dias}
    
    return render(request, 'calendario/add.html', context)

@login_required(login_url='/index/')
def edit(request, calendario_id):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    calendario = Calendario.create(calendario_id)
    
    if request.method == "GET":
        
        dias = []
        
        for dia in calendario.espacio.dias_habiles:
            dias.append(DIAS[dia.dia])
        
        context = {'calendario': calendario, 'dias': dias}
        
        return render(request, 'calendario/edit.html', context)
    
    # Dividimos por 2, esa es la cantidad de atributos.
    for i in range(0, len(request.POST)/2):
        
        horario_id = request.POST[str(i) + '[horario]']
        coordinador_id = request.POST[str(i) + '[coordinador]']
        
        horario = Horario.objects.get(pk=horario_id)
        
        if coordinador_id != "":
            horario.coordinador = Coordinador.objects.get(pk=coordinador_id)
        else:
            horario.coordinador = None
        
        horario.save()
    
    calendario.confirmar()
    
    actividad = Actividad()
    
    actividad.usuario = request.user.username
    actividad.mensaje = "Editó el calendario #" + str(calendario_id)
    
    actividad.save()
    
    data = {"mensaje": "El calendario fue editado exitosamente."}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def delete(request):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        calendario_id = request.POST['calendario_id']
        
        calendario = Calendario.create(calendario_id)
        
        calendario.delete()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Eliminó el calendario #" + str(calendario_id)
        
        actividad.save()
        
        data = {"mensaje": "El calendario se eliminó exitosamente."}
        
    except Exception as ex:
        data = {"error": "No se pudo eliminar el calendario" + str(ex)}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def confirmar(request):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        calendario_id = request.POST['calendario_id']
        
        calendario = Calendario.create(calendario_id)
        
        calendario.confirmar()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Confirmó el calendario #" + str(calendario.id)
        
        actividad.save()
        
        data = {"mensaje": "El calendario se confirmó exitosamente."}
        
    except Exception as ex:
        data = {"error": "No se pudo confirmar el calendario" + str(ex)}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def generar(request):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('index'))
    
    espacio_id = request.POST['espacio_id']
    
    generaciones = cant_generaciones(request.POST['generaciones'])
    
    espacio = Espacio.create(espacio_id)
    
    try:
        
        if espacio.estado == Espacio.GENERANDO:
            return HttpResponseRedirect(reverse('index'))
        
        if espacio.poblacion:
            espacio.poblacion[0].delete()
        
        espacio.estado = Espacio.GENERANDO
        
        espacio.save()
        
        print "Generando población inicial... ",
        sys.stdout.flush()
        
        global_time = time.time()
        
        operation_time = time.time()
        
        # Generamos la población inicial.
        espacio.generarpoblacioninicial()
        
        print " %d individuos en %7.3f seg."\
                % (len(espacio.poblacion), time.time() - operation_time)
        
        print "Evaluando la población... ",
        sys.stdout.flush()
        
        operation_time = time.time()
        
        # Evaluamos la población.
        espacio.fitness(espacio.poblacion)
        
        print " %7.3f seg." % (time.time() - operation_time)
        
        generacion = 0
        
        # Comienza el ciclo de evolución.
        while generacion != generaciones:
            
            generacion += 1
            
            if espacio.progreso != generacion * 100 / generaciones:
                espacio.progreso = generacion * 100 / generaciones
                espacio.save()
            
            print "Generación %d/%d" % (generacion, generaciones)
            
            print "Seleccionando individuos para el cruce... ",
            sys.stdout.flush()
            
            operation_time = time.time()
            
            # Hacemos la seleccion de padres.
            seleccionados = espacio.seleccion()
            
            print " %7.3f seg." % (time.time() - operation_time)
            
            print "Cruzando los individuos... ",
            sys.stdout.flush()
            
            operation_time = time.time()
            
            # Obtenemos los hijos resultantes del cruce.
            hijos = espacio.cruzar(seleccionados)
            
            print " %7.3f seg." % (time.time() - operation_time)
            
            print "Evaluando la nueva población... ",
            sys.stdout.flush()
            
            operation_time = time.time()
            
            # Evaluamos la nueva población.
            espacio.fitness(hijos)
            
            print " %7.3f seg." % (time.time() - operation_time)
            
            print "Hijos generados", len(hijos)
            
            print "Actualizando la población... ",
            sys.stdout.flush()
            
            operation_time = time.time()
            
            # Actualizamos lo individuos de la población.
            espacio.actualizarpoblacion(hijos)
            
            print " %7.3f seg." % (time.time() - operation_time)
            
            print "Grado de la población: ", espacio.grado
            
            print "----------------------------------------------------"
        
        print "Guardando los individuos... ",
        sys.stdout.flush()
        
        operation_time = time.time()
        
        espacio.poblacion[0].full_save()
        
        print " %d individuos en %7.3f seg."\
                % (len(espacio.poblacion), time.time() - operation_time)
        print
        print "La evolución tardó %7.3f seg."\
                % (time.time() - global_time)
        
        mensaje = "Generaste el calendario #%d para el espacio %s"\
                % (espacio.poblacion[0].id, espacio.nombre)
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = mensaje
        
        actividad.save()
        
        data = {'mensaje': "La generación terminó exitosamente."}
        
    except Exception as ex:
        print ex
        
        data = {'error': str(ex).decode('utf-8')}
    
    espacio.estado = Espacio.ON
    espacio.progreso = 0
    
    espacio.save()
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def detail(request, calendario_id):
    
    calendario_id = int(calendario_id)
    
    calendario = None
    
    calendario = get_object_or_404(Calendario, pk=calendario_id)
    calendario = Calendario.create(calendario_id)
    
    anterior = None
    siguiente = None
    
    try:
        anterior = get_object_or_404(Calendario, pk=calendario_id-1)
    except Exception as ex:
        pass
    
    try:
        siguiente = get_object_or_404(Calendario, pk=calendario_id+1)
    except Exception as ex:
        pass
    
    dias = []
    
    for dia in calendario.espacio.dias_habiles:
        dias.append(DIAS[dia.dia])
    
    context = {'calendario': calendario, 'anterior': anterior,
                'siguiente': siguiente, 'dias': dias}
    
    return render(request, 'calendario/detail.html', context)

@login_required(login_url='/index/')
def espacio_all(request, pagina=1):
    
    total_espacios = Espacio.objects.filter(~Q(estado=Espacio.OFF)).order_by('nombre')
    paginator = Paginator(total_espacios, PAGE_LENGTH)
    
    try:
        espacios = paginator.page(pagina)
    except PageNotAnInteger:
        espacios = paginator.page(1)
    except EmptyPage:
        espacios = paginator.page(paginator.num_pages)
    
    context = {'espacios': espacios}
    
    return render(request, 'calendario/espacio/all.html', context)

@login_required(login_url='/index/')
def espacio_detail(request, espacio_id):
    
    espacio = get_object_or_404(Espacio, pk=espacio_id)
    espacio = Espacio.create(espacio_id)
    
    dias = []
    
    for dia in espacio.dias_habiles:
        dias.append(DIAS[dia.dia])
    
    total_horas_especialidades = 0
    for coordinador in espacio.coordinadores.all():
        
        carga = coordinador.especialidad.carga_horaria_semanal
        
        total_horas_especialidades += carga
    
    total_horas = len(espacio.dias_habiles) * len(espacio.horas)
    
    calendario_valido = total_horas == total_horas_especialidades
    
    listo = False
    
    #TO DO: calendario_valido, listo, variables viejas ver que funcion cumplen
    if espacio.coordinadores and calendario_valido:
        listo = True
    
    calendario = None
    
    if Calendario.objects.filter(espacio=espacio):
        
        calendario = Calendario.objects.filter(espacio=espacio)[0]
        
        calendario = Calendario.create(calendario.id)
    
    context = {'espacio': espacio, 'calendario': calendario,
                'dias': dias}
    
    return render(request, 'calendario/espacio/detail.html', context)

@login_required(login_url='/index/')
def espacio_add(request):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method == 'GET':
        return render(request, 'calendario/espacio/add.html')
    
    data = {}
    
    try:
        espacio = Espacio.create()
        
        espacio.setnombre(request.POST["nombre"])
        espacio.usuario_creador = request.user.username
        espacio.usuario_modificador = request.user.username
        
        espacio.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Agregó el espacio " + str(espacio)
        
        actividad.save()
        
        data = {'mensaje': "El espacio ha sido guardado exitosamente.",
                'espacio_id': espacio.id}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'nombre' in str(ex):
            data['campo'] = 'nombre'
        
    finally:
        return JsonResponse(data)

@login_required(login_url='/index/')
def espacio_edit(request, espacio_id=0):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method == 'GET':
        
        espacio = Espacio.create(espacio_id=espacio_id)
        
        context = {'espacio': espacio}
        
        return render(request, 'calendario/espacio/edit.html', context)
    
    data = {}
    
    try:
        
        espacio = Espacio.create(espacio_id)
        
        espacio.setnombre(request.POST['nombre'])
        espacio.usuario_creador = request.user.username
        espacio.usuario_modificador = request.user.username
        
        espacio.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Editó el espacio " + str(espacio)
        
        actividad.save()
        
        data = {'mensaje': "El espacio fue editado exitosamente."}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'nombre' in str(ex):
            data['campo'] = 'nombre'
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def espacio_delete(request):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        espacio = Espacio.create(request.POST['espacio_id'])
        
        espacio.estado = Espacio.OFF
        espacio.usuario_modificador = request.user.username
        
        espacio.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Eliminó el espacio " + str(espacio)
        
        actividad.save()
        
        data = {'mensaje': "El espacio fue eliminado exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def espacio_add_horarios(request, espacio_id=0):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method == 'GET':
        
        espacio = Espacio.create(espacio_id)
        
        horas_select = []
        
        for hora in range(24):
            horas_select.append("%02d" % hora)
        
        min_select = ["00", "05", "10", "15",
                        "20", "25", "30", "35",
                        "40", "45", "50", "55"]
        
        horas = []
        
        if espacio.horas == []:
            for hora in range(6):
                horas.append(hora)
        else:
            for hora in espacio.horas:
                horas.append(str(hora.hora_desde).split(':'))
        
        dias = []
        
        if espacio.dias_habiles == []:
            for dia in range(7):
                dias.append(dia)
        else:
            for dia in espacio.dias_habiles:
                dias.append(str(dia.dia))
        
        context = {'espacio': espacio, 'horas': horas, 'dias': dias,
                    'horas_select': horas_select, 'min_select': min_select}
        
        return render(request, 'calendario/espacio/add_horarios.html', context)
    
    data = {}
    
    try:
        
        espacio = Espacio.create(espacio_id)
        
        for dia in espacio.dias_habiles:
            dia.delete()
        
        for i in range(7):
            
            # Formato de dato 'd0', 'd1', 'd2', etc...
            if request.POST.get('d' + str(i), False):
                
                dia_habil = DiaHabil()
                
                dia_habil.espacio = espacio
                dia_habil.dia = i
                
                dia_habil.save()
                
                espacio.dias_habiles.append(dia_habil)
            
        modulo = request.POST.get("modulo", False)
        
        for hora in espacio.horas:
            hora.delete()
        
        espacio._horas = []
        
        formato = "%H:%M"
        
        i = 0
        for r in request.POST:
            
            # Formato de dato 'h0', 'h1', 'h2', etc...
            if request.POST.get('h' + str(i), False):
                
                # Obtenemos la hora desde.
                hora_desde = request.POST['h' + str(i)]
                hora_desde = datetime.strptime(hora_desde, formato)
                
                # Determinamos la hora hasta con el intervalo "modulo".
                hora_hasta = hora_desde + timedelta(minutes=int(modulo))
                
                hora = Hora()
                
                hora.espacio = espacio
                hora.hora_desde = hora_desde.time()
                hora.hora_hasta = hora_hasta.time()
                
                if not espacio.esHoraValida(hora):
                    
                    error = "La hora no es válida:", str(hora.hora_desde)
                    
                    raise Exception(error)
                
                hora.save()
                
            else:
                break
            
            i += 1
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Modificó los días y las horas del espacio " + str(espacio)
        
        actividad.save()
        
        data = {'mensaje': "Los horarios fueron seteados exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def espacio_add_especialidades(request, espacio_id=0):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    espacio = Espacio.create(espacio_id)
    
    if request.method == 'GET':
        
        especialidades = Especialidad.objects.filter(estado='ON')\
                                                .order_by('nombre')
        
        context = {'espacio': espacio, 'especialidades': especialidades}
        
        return render(request, 'calendario/espacio/add_especialidades.html', context)
    
    data = {}
    
    try:
        
        especialidades = dict(request.POST.iterlists())['especialidades[]']
        
        for especialidad in espacio.especialidades.all():
            espacio.especialidades.remove(especialidad)
        
        for especialidad_id in especialidades:
            
            especialidad = Especialidad.objects.get(pk=especialidad_id)
            
            espacio.especialidades.add(especialidad)
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Modificó las especialidades del espacio " + str(espacio)
        
        actividad.save()
        
        data = {'mensaje': "Las especialidades fueron asignadas exitosamente."}
        
    except KeyError as ex:
        # KeyError 'especialidades[]', vacio todo el arreglo.
        for especialidad in espacio.especialidades.all():
            espacio.especialidades.remove(especialidad)
        
        data = {'mensaje': "Las especialidades fueron removidas exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def espacio_add_profesionales(request, espacio_id=0):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    espacio = Espacio.create(espacio_id)
    
    if request.method == 'GET':
        
        todos_profesionales = Profesional.objects.filter(estado='ON')\
                                                    .order_by('apellido', 'nombre')
        
        profesionales = []
        
        for profesional in todos_profesionales:
            
            for especialidad in espacio.especialidades.all():
                
                if especialidad in profesional.especialidades.all():
                    profesionales.append(profesional)
                    break
        
        context = {'espacio': espacio, 'profesionales': profesionales}
        
        return render(request, 'calendario/espacio/add_profesionales.html', context)
    
    data = {}
    
    try:
        profesionales = dict(request.POST.iterlists())['profesionales[]']
        
        for profesional in espacio.profesionales.all():
            espacio.profesionales.remove(profesional)
        
        coordinadores = Coordinador.objects.filter(espacio=espacio)
        
        for coordinador in coordinadores:
            coordinador.delete()
        
        for profesional in profesionales:
            
            profesional_id, especialidad_id = profesional.split('-')
            
            profesional = Profesional.objects.get(pk=profesional_id)
            
            espacio.profesionales.add(profesional)
            
            especialidad =  Especialidad.create(especialidad_id)
            
            coordinador = Coordinador()
            
            coordinador.espacio = espacio
            coordinador.profesional = profesional
            coordinador.especialidad = especialidad
            
            coordinador.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Modificó los profesionales del espacio " + str(espacio)
        
        actividad.save()
        
        data = {'mensaje': "Los profesionales fueron asignados exitosamente."}
        
    except KeyError as ex:
        # KeyError 'profesionales[]', vacio todo el arreglo.
        for profesional in espacio.profesionales.all():
            espacio.profesionales.remove(profesional)
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def profesional_all(request, pagina=1):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    total_profesionales = Profesional.objects.filter(estado='ON')\
                                            .order_by('apellido', 'nombre')
    paginator = Paginator(total_profesionales, PAGE_LENGTH)
    
    try:
        profesionales = paginator.page(pagina)
    except PageNotAnInteger:
        profesionales = paginator.page(1)
    except EmptyPage:
        profesionales = paginator.page(paginator.num_pages)
    
    context = {'profesionales': profesionales}
    
    return render(request, 'calendario/profesional/all.html', context)

@login_required(login_url='/index/')
def profesional_add(request):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method == 'GET':
        return render(request, 'calendario/profesional/add.html')
    
    data = {}
    
    try:
        profesional = Profesional.create()
        
        tipo = str(request.POST['tipo'])
        documento = str(request.POST['documento'])
        verificador = str(request.POST['verificador'])
        cuil = tipo + "-" + documento + "-" + verificador
        
        profesional.setnombre(request.POST['nombre'])
        profesional.setapellido(request.POST['apellido'])
        profesional.setcuil(cuil)
        profesional.usuario_creador = request.user.username
        profesional.usuario_modificador = request.user.username
        
        profesional.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Agregó el profesional " + str(profesional)
        
        actividad.save()
        
        data = {'mensaje': "El profesional fue guardado exitosamente."}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'nombre' in str(ex):
            data['campo'] = 'nombre'
        
        if 'apellido' in str(ex):
            data['campo'] = 'apellido'
        
        if 'cuil' in str(ex):
            data['campo'] = 'cuil'
        
    finally:
        return JsonResponse(data)

@login_required(login_url='/index/')
def profesional_detail(request, profesional_id):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    profesional = get_object_or_404(Profesional, pk=profesional_id)
    profesional = Profesional.create(profesional_id)
    
    profesional.tipo = profesional.cuil.split('-')[0]
    profesional.documento = profesional.cuil.split('-')[1]
    profesional.verificador = profesional.cuil.split('-')[2]
    
    especialidades = Especialidad.objects.filter(estado='ON')\
                                            .order_by('nombre')
    
    restricciones = []
    for restriccion in profesional.restricciones:
        
        restriccion.nombre_dia_semana = DIAS[restriccion.dia_semana]
        
        restricciones.append(restriccion)
    
    context = {'profesional': profesional,
                'especialidades': especialidades,
                'restricciones': restricciones}
    
    return render(request, 'calendario/profesional/detail.html', context)

@login_required(login_url='/index/')
def profesional_edit(request):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:profesional_all'))
    
    try:
        
        profesional = Profesional.create(request.POST['profesional_id'])
        
        tipo = str(request.POST['tipo'])
        documento = str(request.POST['documento'])
        verificador = str(request.POST['verificador'])
        cuil = tipo + "-" + documento + "-" + verificador
        
        profesional.setnombre(request.POST['nombre'])
        profesional.setapellido(request.POST['apellido'])
        profesional.setcuil(cuil)
        profesional.usuario_modificador = request.user.username
        
        profesional.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Editó el profesional " + str(profesional)
        
        actividad.save()
        
        data = {'mensaje': "El profesional fue editado exitosamente."}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'nombre' in str(ex):
            data['campo'] = 'nombre'
        
        if 'apellido' in str(ex):
            data['campo'] = 'apellido'
        
        if 'cuil' in str(ex):
            data['campo'] = 'cuil'
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def profesional_delete(request):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        profesional = Profesional.create(request.POST['profesional_id'])
        
        profesional.estado = 'OFF'
        profesional.usuario_modificador = request.user.username
        
        profesional.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Eliminó el profesional " + str(profesional)
        
        actividad.save()
        
        data = {'mensaje': "El profesional fue eliminado exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def profesional_add_especialidades(request, ):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        profesional_id = dict(request.POST.iterlists())['profesional_id'][0]
        especialidades = dict(request.POST.iterlists())['especialidades[]']
        
        profesional = Profesional.create(profesional_id)
        
        for especialidad in profesional.especialidades.all():
            profesional.especialidades.remove(especialidad)
        
        for especialidad_id in especialidades:
            
            especialidad = Especialidad.objects.get(pk=especialidad_id)
            
            profesional.especialidades.add(especialidad)
        
        data = {'mensaje': "Las especialidades fueron asignadas exitosamente."}
        
    except KeyError as ex:
        # KeyError 'especialidades[]', vacio todo el arreglo.
        for especialidad in profesional.especialidades.all():
            profesional.especialidades.remove(especialidad)
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def especialidad_all(request, pagina=1):
    
    total_especialidades = None
    
    if request.user.has_perm('auth.profesional'):
        
        total_especialidades = Especialidad.objects.filter(estado='ON', profesional=1)\
                                                    .order_by('nombre')
    else:
        total_especialidades = Especialidad.objects.filter(estado='ON')\
                                                    .order_by('nombre')
    
    paginator = Paginator(total_especialidades, PAGE_LENGTH)
    
    try:
        especialidades = paginator.page(pagina)
    except PageNotAnInteger:
        especialidades = paginator.page(1)
    except EmptyPage:
        especialidades = paginator.page(paginator.num_pages)
    
    context = {'especialidades' : especialidades}
    
    return render(request, 'calendario/especialidad/all.html', context)

@login_required(login_url='/index/')
def especialidad_add(request):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method == 'GET':
        return render(request, 'calendario/especialidad/add.html')
        
    data = {}
    
    try:
        carga_horaria_semanal = request.POST["carga_horaria_semanal"]
        max_horas_diaria = request.POST["max_horas_diaria"]
        
        # TODO si el usuario no quiere que exista un maximo de horas
        # diarias podria querer poner un valor superior...
        if carga_horaria_semanal < max_horas_diaria:
            raise Exception("La carga horaria semanal no puede ser menor que la cantidad de horas.")
        
        especialidad = Especialidad()
        
        especialidad.setnombre(request.POST["nombre"])
        especialidad.setcarga_horaria_semanal(carga_horaria_semanal)
        especialidad.setmax_horas_diaria(max_horas_diaria)
        especialidad.color = request.POST["color"]
        especialidad.usuario_creador = request.user.username
        especialidad.usuario_modificador = request.user.username
        
        especialidad.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Agregó la especialidad " + str(especialidad)
        
        actividad.save()
        
        data = {'mensaje': "La especialidad fue guardada exitosamente."}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'nombre' in str(ex):
            data['campo'] = 'nombre'
        
        if 'semanal' in str(ex):
            data['campo'] = 'carga_horaria_semanal'
        
        if 'diaria' in str(ex):
            data['campo'] = 'max_horas_diaria'
        
    finally:
        return JsonResponse(data)

@login_required(login_url='/index/')
def especialidad_detail(request, especialidad_id):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    especialidad = get_object_or_404(Especialidad, pk=especialidad_id)
    especialidad = Especialidad.create(especialidad_id)
    
    context = {'especialidad': especialidad}
    
    return render(request, 'calendario/especialidad/detail.html', context)

@login_required(login_url='/index/')
def especialidad_edit(request):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method != 'POST':
        return render(request, 'calendario/especialidad/all.html')
    
    data = {}
    
    try:
        especialidad = Especialidad.objects.get(pk=request.POST['especialidad_id'])
        
        especialidad.setnombre(request.POST["nombre"])
        especialidad.setcarga_horaria_semanal(request.POST["carga_horaria_semanal"])
        especialidad.setmax_horas_diaria(request.POST["max_horas_diaria"])
        especialidad.color = request.POST["color"]
        especialidad.usuario_modificador = request.user.username
        
        especialidad.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Editó la especialidad " + str(especialidad)
        
        actividad.save()
        
        data = {'mensaje': "La especialidad fue editada exitosamente."}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'nombre' in str(ex):
            data['campo'] = 'nombre'
        
        if 'semanal' in str(ex):
            data['campo'] = 'carga_horaria_semanal'
        
        if 'diaria' in str(ex):
            data['campo'] = 'max_horas_diaria'
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def especialidad_delete(request):
    
    if request.user.has_perm('auth.profesional'):
        return render(request, 'calendario/denied.html')
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
        
    data = {}
    
    try:
        especialidad_id = request.POST['especialidad_id']
        
        especialidad = Especialidad.objects.get(pk=especialidad_id)
        
        especialidad.estado = 'OFF'
        especialidad.usuario_modificador = request.user.username
        
        especialidad.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Eliminó la especialidad " + str(especialidad)
        
        actividad.save()
        
        data = {'mensaje': "La especialidad fue eliminada exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def restriccion_add(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('index'))
    
    data = {}
    
    try:
        profesional_id = request.POST['profesional_id']
        
        profesional = Profesional.create(profesional_id)
        
        restriccion = Restriccion()
        
        restriccion.profesional = profesional
        restriccion.setdia_semana(request.POST['edit_dia_semana'])
        restriccion.sethora_desde(request.POST['edit_hora_desde'])
        restriccion.sethora_hasta(request.POST['edit_hora_hasta'])
        restriccion.usuario_creador = request.user.username
        restriccion.usuario_modificador = request.user.username
        
        restriccion.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Agregó una restricción para " + str(profesional)
        
        actividad.save()
        
        data = {'mensaje': "La restricción fue asignada exitosamente."}
        data["id"] = restriccion.id
        data["dia_semana"] = DIAS[int(restriccion.dia_semana)]
        data["hora_desde"] = restriccion.hora_desde
        data["hora_hasta"] = restriccion.hora_hasta
        
    except Exception as ex:
        
        data = {'error': str(ex)}
        
        if "tiene un formato inv" in str(ex):
            data = {'error': "El campo tiene un formato inválido."}
        
        if 'hora_hasta' in str(ex) or request.POST['edit_hora_hasta'] in str(ex):
            data['campo'] = 'hora_hasta'
        
        if 'hora_desde' in str(ex) or request.POST['edit_hora_desde'] in str(ex):
            data['campo'] = 'hora_desde'
        
        if 'dia_semana' in str(ex):
            data['campo'] = 'dia_semana'
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def restriccion_edit(request, restriccion_id):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('index'))
    
    data = {}
    
    try:
        
        restriccion = Restriccion.objects.get(pk=restriccion_id)
        
        restriccion.save()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Editó una restricción de " + str(restriccion.profesional)
        
        actividad.save()
        
        data = {'mensaje': "La restricción fue editada exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def restriccion_detail(request, restriccion_id):
    
    restriccion = Restriccion.objects.get(pk=restriccion_id)
    
    context = {'restriccion': restriccion}
    
    return render(request, 'calendario/restriccion/detail.html', context)

@login_required(login_url='/index/')
def restriccion_delete(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('index'))
    
    data = {}
    
    try:
        
        restriccion_id = request.POST['restriccion_id']
        
        restriccion = Restriccion.objects.get(pk=restriccion_id)
        
        #~ restriccion.estado = 'OFF'
        #~ restriccion.usuario_modificador = request.user.username
        
        restriccion.delete()
        
        actividad = Actividad()
        
        actividad.usuario = request.user.username
        actividad.mensaje = "Eliminó una restricción de " + str(restriccion.profesional)
        
        actividad.save()
        
        data = {'mensaje': "La restricción fue eliminada exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

def render_to_pdf(template_src, context_dict):
    
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    
    html = StringIO.StringIO(html.encode("ISO-8859-1"))
    
    pdf = pisa.pisaDocument(html, result)
    
    if pdf.err:
        return HttpResponse('ERROR <pre>%s</pre>' % escape(html))
    
    return HttpResponse(result.getvalue(), content_type='application/pdf')

def imprimir(request, calendario_id):
    
    calendario = Calendario.create(calendario_id)
    
    dias = []
    
    for dia in calendario.espacio.dias_habiles:
        dias.append(DIAS[dia.dia])
    
    context = {"calendario": calendario, "dias": dias}
    
    return render_to_pdf('calendario/imprimir.html', context)

def status(request, espacio_id):
    """
    Recibir por parametro el id del espacio para obtener su estado.
    """
    
    espacio = Espacio.create(espacio_id)
    
    data = {"progreso": espacio.progreso, "estado": espacio.estado}
    
    return JsonResponse(data)

def cant_generaciones(generaciones):
    
    generaciones = int(generaciones)
    
    # Ante problemas más complejos necesitamos más generaciones.
    return 2 ** generaciones * DENSIDAD
