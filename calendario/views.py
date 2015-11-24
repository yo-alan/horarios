# -*- coding: utf-8 -*-
import sys
import time
from threading import Thread
from itertools import groupby

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas

from .models import Calendario
from .models import Profesional
from .models import Horario
from .models import ProfesionalRestriccion
from .models import Especialidad
from .models import Espacio
from .models import Hora
from .models import Coordinador
from .models import DiaHabil

DIAS = {0: 'Domingo', 1: 'Lunes', 2: 'Martes', 3: 'Miércoles',
        4: 'Jueves', 5: 'Viernes', 6: 'Sábado', 7: "Todos los días"}

GENERANDO = False

def index(request):
    
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    return render(request, 'calendario/index.html')

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
        
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    else:
        return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/index/')
def log_out(request):
    
    logout(request)
    
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/index/')
def all(request):
    
    calendarios = Calendario.objects.filter(estado='ON')
    
    context = {'calendarios': calendarios}
    
    return render(request, 'calendario/all.html', context)

@login_required(login_url='/index/')
def add(request, espacio_id):
    
    if request.method == 'POST':
        
        calendario = Calendario.create()
        
        calendario.espacio = Espacio.create(espacio_id)
        
        #Dividimos por 3, esa es la cantidad de atributos.
        #Mas 1 por que el primero es el csrf.
        for i in range(1, len(request.POST)/3+1):
            
            coordinador_id = request.POST[str(i) + '[coordinador]']
            desde = request.POST[str(i) + '[desde]']
            
            coordinador = Coordinador.objects.get(pk=coordinador_id)
            hora = Hora.objects.filter(hora_desde=desde)
            hora = hora.filter(espacio=calendario.espacio.id)
            
            dia_semana = request.POST[str(i) + '[dia]']
            
            #Creamos un horario y los completamos.
            horario = Horario()
            
            horario.profesional = coordinador.profesional
            horario.especialidad = coordinador.especialidad
            horario.hora_desde = hora[0].hora_desde
            horario.hora_hasta = hora[0].hora_hasta
            horario.dia_semana = dia_semana
            
            calendario.agregar_horario(horario)
        
        calendario.full_save()
        
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
    
    if request.method == 'POST':
        
        calendario = Calendario.create(calendario_id)
        
        #Dividimos por 3, esa es la cantidad de atributos.
        #Mas 1 por que el primero es el csrf.
        for i in range(1, len(request.POST)/3+1):
            
            coordinador_id = request.POST[str(i) + '[coordinador]']
            desde = request.POST[str(i) + '[desde]']
            
            coordinador = Coordinador.objects.get(pk=coordinador_id)
            hora = Hora.objects.filter(hora_desde=desde)
            hora = hora.filter(espacio=calendario.espacio.id)
            
            dia_semana = request.POST[str(i) + '[dia]']
            
            #Creamos un horario y los completamos.
            horario = Horario()
            
            horario.profesional = coordinador.profesional
            horario.especialidad = coordinador.especialidad
            horario.hora_desde = hora[0].hora_desde
            horario.hora_hasta = hora[0].hora_hasta
            horario.dia_semana = dia_semana
            
            calendario.agregar_horario(horario)
        
        calendario.full_save()
        
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    calendario = Calendario.create(calendario_id)
    
    dias = []
    
    for dia in calendario.espacio.dias_habiles:
        dias.append(DIAS[dia.dia])
    
    context = {'calendario': calendario, 'dias': dias}
    
    return render(request, 'calendario/edit.html', context)

@login_required(login_url='/index/')
def generar(request):
    
    global GENERANDO
    
    if GENERANDO or request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    GENERANDO = True
    
    espacio_id = request.POST['espacio_id']
    #~ tamanio_poblacion = int(request.POST['tamanio_poblacion']) * 100
    generaciones = int(request.POST['generaciones']) * 500
    
    try:
        
        espacio = Espacio.create(espacio_id)
        
        print "Generando población inicial... ",
        sys.stdout.flush()
        
        global_time = time.time()
        
        operation_time = time.time()
        
        espacio.generarpoblacioninicial()
        
        print " %d individuos en %7.3f seg."\
                % (len(espacio.poblacion), time.time() - operation_time)
        
        print "Evaluando la población... ",
        sys.stdout.flush()
        
        operation_time = time.time()
        
        espacio.fitness(espacio.poblacion)
        
        print " %7.3f seg." % (time.time() - operation_time)
        
        generacion = 0
        
        while generacion != generaciones:
            
            generacion += 1
            
            print "Generación %d/%d" % (generacion, generaciones)
            
            print "Seleccionando individuos para el cruce... ",
            sys.stdout.flush()
            
            operation_time = time.time()
            
            #Hacemos la seleccion de individuos.
            seleccionados = espacio.seleccion()
            
            print " %7.3f seg." % (time.time() - operation_time)
            
            print "Cruzando los individuos... ",
            sys.stdout.flush()
            
            operation_time = time.time()
            
            #Hacemos la seleccion de individuos.
            hijos = espacio.cruzar(seleccionados)
            
            print " %7.3f seg." % (time.time() - operation_time)
            
            print "Evaluando la nueva población... ",
            sys.stdout.flush()
            
            operation_time = time.time()
            
            #Evaluamos la nueva población.
            espacio.fitness(hijos)
            
            print " %7.3f seg." % (time.time() - operation_time)
            
            print "Hijos generados", len(hijos)
            
            print "Actualizando la población... ",
            sys.stdout.flush()
            
            operation_time = time.time()
            
            espacio.actualizarpoblacion(hijos)
            
            print " %7.3f seg." % (time.time() - operation_time)
            
            print "--------------------------------------------------------"
            
        
        print "Guardando los individuos... ",
        sys.stdout.flush()
        
        operation_time = time.time()
        
        for calendario in espacio.poblacion:
            calendario.full_save()
        
        print " %d individuos en %7.3f seg."\
                % (len(espacio.poblacion), time.time() - operation_time)
        print
        print "La evolución tardó %7.3f seg."\
                % (time.time() - global_time)
        
    except Exception as ex:
        print ex
    
    GENERANDO = False

@login_required(login_url='/index/')
def detail(request, calendario_id):
    
    calendario = Calendario.create(calendario_id)
    
    espacio = Espacio.create(espacio_id=calendario.espacio.id)
    
    anterior = None
    siguiente = None
    
    try:
        anterior = get_object_or_404(Calendario, pk=int(calendario_id)-1)
    except Exception as ex:
        print ex
    
    try:
        siguiente = get_object_or_404(Calendario, pk=int(calendario_id)+1)
    except Exception as ex:
        print ex
    
    espacio = Espacio.create(espacio_id=calendario.espacio.id)
    
    dias = []
    
    for dia in espacio.dias_habiles:
        dias.append(DIAS[dia.dia])
    
    context = {'calendario': calendario, 'anterior': anterior,
                'siguiente': siguiente, 'dias': dias}
    
    return render(request, 'calendario/detail.html', context)

@login_required(login_url='/index/')
def espacio_all(request, pagina=1):
    
    total_espacios = Espacio.objects.filter(estado='ON').order_by('nombre')
    paginator = Paginator(total_espacios, 10)
    
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
    
    global GENERANDO
    
    espacio = Espacio.create(espacio_id)
    
    especialidades = Especialidad.objects.filter(estado='ON')\
                                            .order_by('nombre')
    
    todas_profesionales = Profesional.objects.filter(estado='ON')\
                                                .order_by('apellido', 'nombre')
    
    #Muestro solo los profesionales que ejercen
    #las especialidades asignadas al espacio.
    profesionales = []
    
    for profesional in todas_profesionales:
        
        for especialidad in espacio.especialidades.all():
            
            if especialidad in profesional.especialidades.all():
                profesionales.append(profesional)
    
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
    
    if espacio.coordinadores and calendario_valido:
        listo = True
    
    context = {'espacio': espacio, 'especialidades': especialidades,
                'profesionales': profesionales, 'dias': dias,
                'listo': listo, 'GENERANDO': GENERANDO}
    
    return render(request, 'calendario/espacio/detail.html', context)

@login_required(login_url='/index/')
def espacio_add(request):
    
    if request.method == 'GET':
        return render(request, 'calendario/espacio/add.html')
    
    data = {}
    
    try:
        espacio = Espacio.create()
        
        espacio.setnombre(request.POST["nombre"])
        
        espacio.save()
        
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
    
    if request.method == 'GET':
        
        espacio = Espacio.create(espacio_id=espacio_id)
        
        context = {'espacio': espacio}
        
        return render(request, 'calendario/espacio/edit.html', context)
    
    data = {}
    
    try:
        #~ espacio = Espacio.create(request.POST['espacio_id'])
        espacio = Espacio.create(espacio_id)
        
        espacio.setnombre(request.POST['nombre'])
        
        espacio.save()
        
        data = {'mensaje': "El espacio fue editado exitosamente."}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'nombre' in str(ex):
            data['campo'] = 'nombre'
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def espacio_delete(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        espacio = Espacio.create(request.POST['espacio_id'])
        
        espacio.estado = 'OFF'
        
        espacio.save()
        
        data = {'mensaje': "El espacio fue eliminado exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def espacio_add_horarios(request, espacio_id=0):
    
    if request.method == 'GET':
        
        espacio = Espacio.create(espacio_id)
        
        horas = []
        
        for hora in range(24):
            horas.append("%02d" % hora)
        
        context = {'espacio': espacio, 'horas': horas}
        
        return render(request, 'calendario/espacio/add_horarios.html', context)
    
    data = {}
    
    try:
        
        espacio = Espacio.create(request.POST['espacio_id'])
        
        hora = Hora()
        
        hora_desde = request.POST['hora_desde']
        min_desde = request.POST['min_desde']
        
        hora_hasta = request.POST['min_hasta']
        min_hasta = request.POST['min_hasta']
        
        hora.hora_desde = hora_desde + ":" + min_desde
        hora.hora_hasta = hora_hasta + ":" + min_hasta
        
        if hora.hora_desde == hora.hora_hasta:
            raise Exception("Las horas no pueden ser iguales.")
        
        hora.espacio = espacio
        
        hora.save()
        
        data = {'mensaje': "La hora fue agregada exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

def espacio_add_dias(request, espacio_id=0):
    
    if request.method == 'GET':
        
        espacio = Espacio.create(espacio_id)
        
        context = {'espacio': espacio}
        
        return render(request, 'calendario/espacio/add_dias.html', context)
    
    data = {}
    
    try:
        espacio = Espacio.create(request.POST['espacio_id'])
        
        for dia in espacio.dias_habiles:
            dia.delete()
        
        for i in range(7):
            
            if request.POST.get('dia_' + str(i), False):
                
                dia_habil = DiaHabil()
                
                dia_habil.espacio = espacio
                dia_habil.dia = i
                
                dia_habil.save()
                
                espacio.dias_habiles.append(dia_habil)
            
        data = {'mensaje': "Los dias fueron agregados exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def espacio_add_especialidades(request, espacio_id=0):
    
    espacio = Espacio.create(espacio_id)
    
    if request.method == 'GET':
        
        especialidades = Especialidad.objects.filter(estado='ON')\
                                                .order_by('nombre')
        
        context = {'espacio': espacio, 'especialidades': especialidades}
        
        return render(request, 'calendario/espacio/add_especialidades.html', context)
    
    data = {}
    
    try:
        
        especialidades = dict(request.POST.iterlists())['especialidades[]']
        
        for especialidad in espacio.especialidades.filter(estado='ON'):
            espacio.especialidades.remove(especialidad)
        
        for especialidad in especialidades:
            espacio.especialidades.add(Especialidad.objects.get(pk=especialidad))
        
        data = {'mensaje': "Las especialidades fueron asignadas exitosamente."}
        
    except KeyError as ex:
        #KeyError 'especialidades[]', vacio todo el arreglo.
        for especialidad in espacio.especialidades.filter(estado='ON'):
            espacio.especialidades.remove(especialidad)
        
        data = {'mensaje': "Las especialidades fueron removidas exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def espacio_add_profesionales(request, espacio_id=0):
    
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
        
        for profesional in espacio.profesionales.filter(estado='ON'):
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
        
        data = {'mensaje': "Los profesionales fueron asignados exitosamente."}
        
    except KeyError as ex:
        #KeyError 'profesionales[]', vacio todo el arreglo.
        for profesional in espacio.profesionales.filter(estado='ON'):
            espacio.profesionales.remove(profesional)
        #~ 
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def profesional_all(request, pagina=1):
    
    total_profesionales = Profesional.objects.filter(estado='ON')\
                                            .order_by('apellido', 'nombre')
    paginator = Paginator(total_profesionales, 10)
    
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
    
    if request.method == 'GET':
        return render(request, 'calendario/profesional/add.html')
    
    data = {}
    
    try:
        profesional = Profesional.create()
        
        profesional.setnombre(request.POST['nombre'])
        profesional.setapellido(request.POST['apellido'])
        profesional.setcuil(request.POST['cuil'])
        
        profesional.save()
        
        data = {'mensaje': "El profesional ha sido guardado exitosamente."}
        
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
    
    profesional = Profesional.create(profesional_id)
    
    especialidades = Especialidad.objects.filter(estado='ON')\
                                            .order_by('nombre')
    
    restricciones = []
    for restriccion in profesional.restricciones:
        
        restriccion.nombre_dia_semana = DIAS[restriccion.dia_semana]
        
        restricciones.append(restriccion)
    
    #TODO DIAS
    context = {'profesional': profesional,
                'especialidades': especialidades,
                'restricciones': restricciones}
    
    return render(request, 'calendario/profesional/detail.html', context)

@login_required(login_url='/index/')
def profesional_edit(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    try:
        
        profesional = Profesional.create(request.POST['profesional_id'])
        
        profesional.setnombre(request.POST['nombre'])
        profesional.setapellido(request.POST['apellido'])
        profesional.setcuil(request.POST['cuil'])
        
        profesional.save()
        
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
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        profesional = Profesional.create(request.POST['profesional_id'])
        
        profesional.estado = 'OFF'
        
        profesional.save()
        
        data = {'mensaje': "El profesional fue eliminado exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def profesional_add_especialidades(request, ):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        profesional_id = dict(request.POST.iterlists())['profesional_id'][0]
        especialidades = dict(request.POST.iterlists())['especialidades[]']
        
        profesional = Profesional.create(profesional_id)
        
        for especialidad in profesional.especialidades.filter(estado='ON'):
            profesional.especialidades.remove(especialidad)
        
        for especialidad in especialidades:
            profesional.especialidades.add(Especialidad.objects.get(pk=especialidad))
        
        data = {'mensaje': "Las especialidades fueron asignadas exitosamente."}
        
    except KeyError as ex:
        #KeyError 'especialidades[]', vacio todo el arreglo.
        for especialidad in profesional.especialidades.filter(estado='ON'):
            profesional.especialidades.remove(especialidad)
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def profesional_add_restriccion(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        profesional_id = request.POST['profesional_id']
        
        profesional = Profesional.create(profesional_id)
        
        restriccion = ProfesionalRestriccion()
        
        restriccion.setprofesional(profesional)
        restriccion.setdia_semana(request.POST['dia_semana'])
        restriccion.sethora_desde(request.POST['hora_desde'])
        restriccion.sethora_hasta(request.POST['hora_hasta'])
        
        restriccion.save()
        
        data = {'mensaje': "La restricción fue asignada exitosamente."}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'hora_hasta' in str(ex) or request.POST['hora_hasta'] in str(ex):
            data['campo'] = 'hora_hasta'
        
        if 'hora_desde' in str(ex) or request.POST['hora_desde'] in str(ex):
            data['campo'] = 'hora_desde'
        
        if 'dia_semana' in str(ex):
            data['campo'] = 'dia_semana'
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def especialidad_all(request, pagina=1):
    
    total_especialidades = Especialidad.objects.filter(estado='ON')\
                                                .order_by('nombre')
    paginator = Paginator(total_especialidades, 10)
    
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
    
    if request.method == 'GET':
        return render(request, 'calendario/especialidad/add.html')
        
    data = {}
    
    try:
        especialidad = Especialidad()
        
        especialidad.setnombre(request.POST["nombre"])
        especialidad.setcarga_horaria_semanal(request.POST["carga_horaria_semanal"])
        especialidad.setmax_horas_diaria(request.POST["max_horas_diaria"])
        especialidad.color = request.POST["color"]
        
        if especialidad.carga_horaria_semanal < especialidad.max_horas_diaria:
            raise Exception("La carga horaria semanal no puede ser menor que la cantidad de horas.")
        
        especialidad.save()
        
        data = {'mensaje': "La especialidad ha sido guardada exitosamente."}
        
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
    
    especialidad = Especialidad.create(especialidad_id)
    
    context = {'especialidad': especialidad}
    
    return render(request, 'calendario/especialidad/detail.html', context)

@login_required(login_url='/index/')
def especialidad_edit(request):
    
    if request.method != 'POST':
        return render(request, 'calendario/especialidad/all.html')
    
    data = {}
    
    try:
        especialidad = Especialidad.objects.get(pk=request.POST['especialidad_id'])
        
        especialidad.setnombre(request.POST["nombre"])
        especialidad.setcarga_horaria_semanal(request.POST["carga_horaria_semanal"])
        especialidad.setmax_horas_diaria(request.POST["max_horas_diaria"])
        especialidad.color = request.POST["color"]
        
        especialidad.save()
        
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
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
        
    data = {}
    
    try:
        especialidad = Especialidad.objects.get(pk=request.POST['especialidad_id'])
        
        especialidad.estado = 'OFF'
        
        especialidad.save()
        
        data = {'mensaje': "La especialidad fue eliminada exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def restriccion_add(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        restriccion = Restriccion()
        
        restriccion.setnombre(request.POST["nombre"])
        restriccion.setcarga_horaria_semanal(request.POST["carga_horaria_semanal"])
        restriccion.setmax_horas_diaria(request.POST["max_horas_diaria"])
        
        if restriccion.carga_horaria_semanal < restriccion.max_horas_diaria:
            raise Exception("La carga horaria semanal no puede ser menor que la cantidad de horas.")
        
        restriccion.save()
        
        data = {'mensaje': "La especialidad ha sido guardada exitosamente."}
        
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
def restriccion_edit(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        
        especialidad = Especialidad.objects.get(pk=especialidad_id)
        
        especialidad.nombre = request.POST["nombre"]
        especialidad.carga_horaria_semanal = request.POST["carga_horaria_semanal"]
        especialidad.max_horas_diaria = request.POST["max_horas_diaria"]
        
        especialidad.save()
        
        data = {'mensaje': "La restricción fue editada exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def restriccion_delete(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        restriccion = Especialidad.objects.get(pk=request.POST['especialidad_id'])
        
        restriccion.estado = 'OFF'
        
        restriccion.save()
        
        data = {'mensaje': "El profesional fue eliminado exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

@login_required(login_url='/index/')
def getrestriccionesof(request):
    
    if request.method != 'GET':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        
        profesional = Profesional.create(request.GET['profesional_id'])
        
        data = serializers.serialize('json', profesional.restricciones.filter(estado='ON'))
        
        print data
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
