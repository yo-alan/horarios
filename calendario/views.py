# -*- coding: utf-8 -*-
import time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Entorno, Calendario, Profesional, Horario, ProfesionalRestriccion, EspacioRestriccion, Especialidad, Espacio, Hora

DIAS = {0 : 'Domingo', 1 : 'Lunes', 2 : 'Martes', 3 : 'Miércoles', 4 : 'Jueves', 5 : 'Viernes', 6 : 'Sábado'}

def index(request):
	
	context = {}
	
	return render(request, 'calendario/index.html', context)

def all(request):
	
	calendarios = Calendario.objects.all()
	
	context = {'calendarios': calendarios}
	
	return render(request, 'calendario/all.html', context)

def add(request, espacio_id):
	
	if request.method == 'POST':
		
		calendario = Calendario.create()
		
		calendario.espacio = Espacio.create(espacio_id)
		calendario.save()
		
		#Dividimos por 3 por esa es la cantidad de atributos y mas 1 por que el primero es el csrf.
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
	
	colores = ['#337ab7', '#5cb85c', '#5bc0de', '#f0ad4e', '#d9534f', '#73e673', '#ffc879', '#ff625c', '#', '#', '#', '#', '#', '#', '#', '#']
	
	context = {'espacio': espacio, 'dias': dias, 'colores': colores}
	
	return render(request, 'calendario/add.html', context)

def generar(request):
	
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('calendario:all'))
	
	start_time = time.time()
	
	espacio = Espacio.create(request.POST['espacio_id'])
	
	entorno = Entorno(espacio=espacio)
	
	entorno.generar_poblacion_inicial()
	
	entorno.evolucionar()
	
	tiempo = (time.time() - start_time)
	
	context = {'calendarios': entorno.poblacion, 'tiempo': tiempo}
	
	return render(request, 'calendario/all.html', context)

def detail(request, calendario_id):
	
	calendario = Calendario.create(calendario_id)
	
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
	
	context = {'calendario': calendario, 'dias': range(5), 'horas': range(6), 'anterior': anterior, 'siguiente': siguiente}
	
	return render(request, 'calendario/detail.html', context)

def espacio_all(request, pagina=1):
	
	total_espacios = Espacio.objects.all().order_by('nombre')
	paginator = Paginator(total_espacios, 10)
	
	try:
		espacios = paginator.page(pagina)
	except PageNotAnInteger:
		espacios = paginator.page(1)
	except EmptyPage:
		espacios = paginator.page(paginator.num_pages)
	
	context = {'espacios': espacios, }
	
	return render(request, 'calendario/espacio/all.html', context)

def espacio_detail(request, espacio_id):
	
	espacio = Espacio.create(espacio_id)
	
	especialidades = Especialidad.objects.all().order_by('nombre')
	
	context = {'espacio': espacio, 'especialidades': especialidades}
	
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
		
		data = {'mensaje', "El espacio fue editado exitosamente."}
		
	except Exception as ex:
		
		data = {'error', str(ex).decode('utf-8')}
		
		if 'nombre' in str(ex):
			data['campo'] = 'nombre'
	
	return JsonResponse(data)

def espacio_delete(request):
	
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('calendario:espacio_all'))
	
	data = {}
	
	try:
		espacio = Espacio.create(request.POST['espacio_id'])
		
		espacio.delete()
		
		data = {'mensaje', "El espacio fue eliminado exitosamente."}
		
	except Exception as ex:
		data = {'error', str(ex).decode('utf-8')}
	
	return JsonResponse(data)

def espacio_horas(request, espacio_id):
	
	context = {}
	
	espacio = Espacio.create(espacio_id)
	
	context['espacio'] = espacio
	
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

def espacio_add_especialidades(request, ):
	
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('calendario:espacio_all'))
	
	data = {}
	
	try:
		espacio_id = dict(request.POST.iterlists())['espacio_id'][0]
		especialidades = dict(request.POST.iterlists())['especialidades[]']
		
		espacio = Espacio.create(espacio_id)
		
		for especialidad in espacio.especialidades.all():
			espacio.especialidades.remove(especialidad)
		
		for especialidad in especialidades:
			espacio.especialidades.add(Especialidad.objects.get(pk=especialidad))
		
		data = {'mensaje': "Las especialidades fueron asignadas exitosamente."}
		
	except KeyError as ex:
		#KeyError 'especialidades[]', vacio todo el arreglo.
		for especialidad in espacio.especialidades.all():
			espacio.especialidades.remove(especialidad)
		
	except Exception as ex:
		data = {'error': str(ex).decode('utf-8')}
	
	return JsonResponse(data)

def profesional_all(request, pagina=1):
	
	total_profesionales = Profesional.objects.all().order_by('apellido', 'nombre')
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
		profesional = Profesional()
		
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
	
	context = {}
	
	profesional = Profesional.objects.get(pk=profesional_id)
	
	if request.method == 'POST':
		
		try:
			profesional.nombre = request.POST["nombre"]
			profesional.apellido = request.POST["apellido"]
			profesional.cuil = request.POST["cuil"]
			profesional.especialidad = Especialidad.objects.get(pk=request.POST["especialidad"])
			
			profesional.save()
			
			return HttpResponseRedirect(reverse('calendario:profesional_all'))
			
		except Exception as ex:
			context['error_message'] = "Error editando el profesional: " + str(ex)
	
	especialidades = Especialidad.objects.all().order_by('nombre')
	
	context['profesional'] = profesional
	context['especialidades'] = especialidades
	
	return render(request, 'calendario/profesional/detail.html', context)

def profesional_edit(request):
	
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('calendario:profesional_all'))
	
	try:
		
		profesional = Profesional.objects.get(pk=request.POST['profesional_id'])
		
		profesional.setnombre(request.POST['nombre'])
		profesional.setapellido(request.POST['apellido'])
		profesional.setcuil(request.POST['cuil'])
		
		profesional.save()
		
	except Exception as ex:
		
		data = {'error', str(ex).decode('utf-8')}
		
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
		profesional = Profesional.objects.get(pk=request.POST['profesional_id'])
		
		profesional.delete()
		
		data = {'mensaje', "El profesional fue eliminado exitosamente."}
		
	except Exception as ex:
		data = {'error', str(ex).decode('utf-8')}
	
	return JsonResponse(data)

def profesional_add_especialidades(request, ):
	
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('calendario:profesional_all'))
	
	data = {}
	
	try:
		profesional_id = dict(request.POST.iterlists())['profesional_id'][0]
		especialidades = dict(request.POST.iterlists())['especialidades[]']
		
		profesional = Profesional.objects.get(pk=profesional_id)
		
		for especialidad in profesional.especialidades.all():
			profesional.especialidades.remove(especialidad)
		
		for especialidad in especialidades:
			profesional.especialidades.add(Especialidad.objects.get(pk=especialidad))
		
		data = {'mensaje': "Las especialidades fueron asignadas exitosamente."}
		
	except KeyError as ex:
		#KeyError 'especialidades[]', vacio todo el arreglo.
		for especialidad in profesional.especialidades.all():
			profesional.especialidades.remove(especialidad)
		
	except Exception as ex:
		data = {'error': str(ex).decode('utf-8')}
	
	return JsonResponse(data)

def profesional_add_restriccion(request, ):
	
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('calendario:profesional_all'))
	
	data = {}
	
	try:
		profesional_id = request.POST['profesional_id']
		
		profesional = Profesional.objects.get(pk=profesional_id)
		
		restriccion = ProfesionalRestriccion()
		
		restriccion.setprofesional(profesional)
		restriccion.setdia_semana(request.POST['dia_semana'])
		restriccion.sethora_desde(request.POST['hora_desde'])
		restriccion.sethora_hasta(request.POST['hora_hasta'])
		
		data = {'mensaje': "Las especialidades fueron asignadas exitosamente."}
		
	except Exception as ex:
		
		data = {'error': str(ex).decode('utf-8')}
		
		if 'dia_semana' in str(ex):
			data['campo'] = 'dia_semana'
		
		if 'hora_desde' in str(ex):
			data['campo'] = 'hora_desde'
		
		if 'hora_hasta' in str(ex):
			data['campo'] = 'hora_hasta'
	
	return JsonResponse(data)

def especialidad_all(request, pagina=1):
	
	total_especialidades = Especialidad.objects.all().order_by('nombre')
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

def especialidad_edit(request):
	
	context = {}
	
	especialidad = Especialidad.objects.get(pk=request.POST['especialidad_id'])
	
	if request.method == 'GET':
		
		context['especialidad'] = especialidad
		
		return render(request, 'calendario/especialidad/edit.html', context)
	
	data = {}
	
	try:
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
		
		especialidad.delete()
		
		data = {'mensaje', "La especialidad fue eliminada exitosamente."}
		
	except Exception as ex:
		data = {'error', str(ex).decode('utf-8')}
	
	return JsonResponse(data)

def restriccion_all(request, pagina=1):
	
	total_restricciones = Restriccion.objects.all().order_by('nombre')
	paginator = Paginator(total_restricciones, 10)
	
	try:
		restricciones = paginator.page(pagina)
	except PageNotAnInteger:
		restricciones = paginator.page(1)
	except EmptyPage:
		restricciones = paginator.page(paginator.num_pages)
	
	context = {'restricciones' : restricciones}
	
	return render(request, 'calendario/restriccion/all.html', context)

def restriccion_add(request):
	
	if request.method == 'GET':
		context = {}
		
		return render(request, 'calendario/restriccion/add.html', context)
		
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
	
	if request.method == 'GET':
		context = {}
	
		return render(request, 'calendario/restriccion/edit.html', context)
	
	data = {}
	
	try:
		
		especialidad = Especialidad.objects.get(pk=especialidad_id)
		
		especialidad.nombre = request.POST["nombre"]
		especialidad.carga_horaria_semanal = request.POST["carga_horaria_semanal"]
		especialidad.max_horas_diaria = request.POST["max_horas_diaria"]
		
		especialidad.save()
		
		data = {'mensaje', "La restricción fue editada exitosamente."}
		
	except Exception as ex:
		data = {'error', str(ex).decode('utf-8')}
	
	return JsonResponse(data)

def restriccion_delete(request):
	
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('calendario:especialidad_all'))
		
	data = {}
	
	try:
		especialidad = Especialidad.objects.get(pk=request.POST['especialidad_id'])
		
		especialidad.delete()
		
		data = {'mensaje', "El profesional fue eliminado exitosamente."}
		
	except Exception as ex:
		data = {'error', str(ex).decode('utf-8')}
	
	return JsonResponse(data)
