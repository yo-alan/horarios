# -*- coding: utf-8 -*-
import sys
import time

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Calendario
from .models import Profesional
from .models import Horario
from .models import ProfesionalRestriccion
from .models import Especialidad
from .models import Espacio
from .models import Hora

DIAS = {0: 'Domingo', 1: 'Lunes', 2: 'Martes', 3: 'Miércoles',
        4: 'Jueves', 5: 'Viernes', 6: 'Sábado', 7: "Todos los días"}

COLORES = ['#FE2E2E', '#FF8000', '#01DF3A', '#0080FF', '#F78181',
            '#F7BE81', '#2EFE64', '#58ACFA', '#FA5882', '#FFBF00']

def index(request):
    
    context = {}
    
    return render(request, 'calendario/index.html', context)

def acerca(request):
    
    context = {}
    
    return render(request, 'calendario/acerca.html', context)

def all(request):
    
    calendarios = Calendario.objects.filter(estado='ON')
    
    context = {'calendarios': calendarios}
    
    return render(request, 'calendario/all.html', context)

def add(request, espacio_id):
    
    if request.method == 'POST':
        
        calendario = Calendario.create()
        
        calendario.espacio = Espacio.create(espacio_id)
        calendario.save()
        
        #Dividimos por 3, esa es la cantidad de atributos. Mas 1 por que el primero es el csrf.
        for i in range(1, len(request.POST)/3+1):
            
            #Creamos un horario y los completamos.
            horario = Horario()
            
            horario.calendario = calendario
            horario.profesional = request.POST[str(i) + '[especialidad]']
            horario.desde = request.POST[str(i) + '[desde]']
            horario.dia_semana = request.POST[str(i) + '[dia]']
            
            horario.save()
        
        return HttpResponseRedirect(reverse('calendario:all'))
    
    espacio = Espacio.create(espacio_id)
    
    dias = []
    
    for num in DIAS:
        if num in espacio.dias_habiles:
            dias.append(DIAS[num])
    
    especialidades = []
    i = 0
    for especialidad in espacio.especialidades.all():
        
        especialidad.color = COLORES[i]
        
        especialidades.append(especialidad)
        
        i += 1
    
    context = {'espacio': espacio, 'dias': dias,
                'especialidades': especialidades}
    
    return render(request, 'calendario/add.html', context)

def generar(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:all'))
    
    espacio = Espacio.create(request.POST['espacio_id'])
    
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
    
    for i in range(20):
        
        print i
        
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
        
        print len(hijos)
        
        print " %7.3f seg." % (time.time() - operation_time)
        
        print "Actualizando la población... ",
        sys.stdout.flush()
        
        operation_time = time.time()
        
        espacio.actualizarpoblacion(hijos)
        
        print " %7.3f seg." % (time.time() - operation_time)
    
    
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
    
    context = {'calendarios': espacio.poblacion}
    
    return render(request, 'calendario/all.html', context)

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
    
    for num in DIAS:
        if num in espacio.dias_habiles:
            dias.append(DIAS[num])
    
    especialidades = []
    i = 0
    for especialidad in espacio.especialidades.all():
        
        especialidad.color = COLORES[i]
        
        especialidades.append(especialidad)
        
        i += 1
    
    context = {'calendario': calendario, 'anterior': anterior,
                'siguiente': siguiente, 'dias': dias,
                'especialidades': especialidades}
    
    return render(request, 'calendario/detail.html', context)

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

def espacio_detail(request, espacio_id):
    
    espacio = Espacio.create(espacio_id)
    
    especialidades = Especialidad.objects.filter(estado='ON')\
                                            .order_by('nombre')
    
    todas_profesionales = Profesional.objects.filter(estado='ON')\
                                                .order_by('apellido', 'nombre')
    
    #Muestro solo los profesionales que ejercen las especialidades asignadas al espacio.
    profesionales = []
    
    for profesional in todas_profesionales:
        
        for especialidad in espacio.especialidades.all():
            
            if especialidad in profesional.especialidades.all():
                profesionales.append(profesional)
    
    dias = []
    
    for num in DIAS:
        if num in espacio.dias_habiles:
            dias.append(DIAS[num])
    
    total_horas_especialidades = 0
    for especialidad in especialidades:
        total_horas_especialidades += especialidad.carga_horaria_semanal
    
    total_horas_calculadas = len(espacio.dias_habiles) * len(espacio.horas)
    
    calendario_valido = total_horas_calculadas == total_horas_especialidades
    
    listo = False
    #~ if espacio.coordinadores and espacio.horas and dias and calendario_valido:
    if espacio.coordinadores and espacio.horas and dias:
        listo = True
    
    context = {'espacio': espacio, 'especialidades': especialidades,
                'profesionales': profesionales, 'dias': dias,
                'listo': listo}
    
    return render(request, 'calendario/espacio/detail.html', context)

def espacio_add(request):
    
    if request.method == 'GET':
        context = {}
        
        return render(request, 'calendario/espacio/add.html', context)
    
    data = {}
    
    try:
        espacio = Espacio.create()
        
        espacio.setnombre(request.POST["nombre"])
        
        espacio.save()
        
        data = {'mensaje': "El espacio ha sido guardado exitosamente."}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'nombre' in str(ex):
            data['campo'] = 'nombre'
        
    finally:
        return JsonResponse(data)
    
def espacio_edit(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        espacio = Espacio.create(request.POST['espacio_id'])
        
        espacio.setnombre(request.POST['nombre'])
        
        espacio.save()
        
        data = {'mensaje': "El espacio fue editado exitosamente."}
        
    except Exception as ex:
        
        data = {'error': str(ex).decode('utf-8')}
        
        if 'nombre' in str(ex):
            data['campo'] = 'nombre'
    
    return JsonResponse(data)

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

def espacio_horas(request, espacio_id):
    
    espacio = Espacio.create(espacio_id)
    
    context = {'espacio': espacio}
    
    return render(request, 'calendario/espacio/horas.html', context)

def espacio_add_hora(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    try:
        
        espacio = Espacio.create(request.POST['espacio_id'])
        
        hora = Hora()
        
        hora.hora_desde = request.POST['hora_desde'] + ":" + request.POST['min_desde']
        hora.hora_hasta = request.POST['hora_hasta'] + ":" + request.POST['min_hasta']
        
        if hora.hora_desde == hora.hora_hasta:
            raise Exception("Las horas no pueden ser iguales.")
        
        hora.espacio = espacio
        
        hora.save()
        
        return JsonResponse({'mensaje': "La hora fue agregada exitosamente."})
        
    except Exception as ex:
        return JsonResponse({'error': str(ex).decode('utf-8')})

def espacio_add_especialidades(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    espacio_id = dict(request.POST.iterlists())['espacio_id'][0]
    espacio = Espacio.create(espacio_id)
    
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

def espacio_add_profesionales(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:espacio_all'))
    
    data = {}
    
    try:
        espacio_id = dict(request.POST.iterlists())['espacio_id'][0]
        profesionales = dict(request.POST.iterlists())['profesionales[]']
        
        espacio = Espacio.create(espacio_id)
        
        for profesional in espacio.profesionales.filter(estado='ON'):
            espacio.profesionales.remove(profesional)
        
        for profesional in profesionales:
            espacio.profesionales.add(Profesional.objects.get(pk=profesional))
        
        data = {'mensaje': "Los profesionales fueron asignados exitosamente."}
        
    except KeyError as ex:
        #KeyError 'profesionales[]', vacio todo el arreglo.
        for profesional in espacio.profesionales.filter(estado='ON'):
            espacio.profesionales.remove(profesional)
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

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

def profesional_add(request):
    
    if request.method == 'GET':
        context = {}
    
        return render(request, 'calendario/profesional/add.html', context)
    
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

def profesional_edit(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:profesional_all'))
    
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

def profesional_delete(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:profesional_all'))
    
    data = {}
    
    try:
        profesional = Profesional.create(request.POST['profesional_id'])
        
        profesional.estado = 'OFF'
        
        profesional.save()
        
        data = {'mensaje': "El profesional fue eliminado exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

def profesional_add_especialidades(request, ):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:profesional_all'))
    
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

def profesional_add_restriccion(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:profesional_all'))
    
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

def especialidad_add(request):
    
    if request.method == 'GET':
        context = {}
        
        return render(request, 'calendario/especialidad/add.html', context)
        
    data = {}
    
    try:
        especialidad = Especialidad()
        
        especialidad.setnombre(request.POST["nombre"])
        especialidad.setcarga_horaria_semanal(request.POST["carga_horaria_semanal"])
        especialidad.setmax_horas_diaria(request.POST["max_horas_diaria"])
        
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

def especialidad_detail(request, especialidad_id):
    
    especialidad = Especialidad.create(especialidad_id)
    
    context = {'especialidad': especialidad}
    
    return render(request, 'calendario/especialidad/detail.html', context)

def especialidad_edit(request):
    
    if request.method != 'POST':
        context = {}
        
        return render(request, 'calendario/especialidad/all.html', context)
    
    data = {}
    
    try:
        especialidad = Especialidad.objects.get(pk=request.POST['especialidad_id'])
        
        especialidad.setnombre(request.POST["nombre"])
        especialidad.setcarga_horaria_semanal(request.POST["carga_horaria_semanal"])
        especialidad.setmax_horas_diaria(request.POST["max_horas_diaria"])
        
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

def especialidad_delete(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:especialidad_all'))
        
    data = {}
    
    try:
        especialidad = Especialidad.objects.get(pk=request.POST['especialidad_id'])
        
        especialidad.estado = 'OFF'
        
        especialidad.save()
        
        data = {'mensaje': "La especialidad fue eliminada exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

def restriccion_add(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:profesional_all'))
    
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

def restriccion_edit(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:profesional_all'))
    
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

def restriccion_delete(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calendario:profesional_all'))
    
    data = {}
    
    try:
        restriccion = Especialidad.objects.get(pk=request.POST['especialidad_id'])
        
        restriccion.estado = 'OFF'
        
        restriccion.save()
        
        data = {'mensaje': "El profesional fue eliminado exitosamente."}
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)

def getrestriccionesof(request):
    
    if request.method != 'GET':
        return HttpResponseRedirect(reverse('calendario:profesional_all'))
    
    data = {}
    
    try:
        
        profesional = Profesional.create(request.GET['profesional_id'])
        
        data = serializers.serialize('json', profesional.restricciones.filter(estado='ON'))
        
        print data
        
    except Exception as ex:
        data = {'error': str(ex).decode('utf-8')}
    
    return JsonResponse(data)
