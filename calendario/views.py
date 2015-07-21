import time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Entorno, Calendario, Profesional, Horario, Restriccion, Especialidad, Espacio

entorno = None

def index(request):
	
	context = {}
	
	return render(request, 'calendario/index.html', context)

def all(request):
	
	calendarios = Calendario.objects.all()
	
	context = {'calendarios': calendarios, 'cantidad': len(calendarios)}
	
	return render(request, 'calendario/all.html', context)

def add(request):
	
	entorno = Entorno(espacio=Espacio.objects.get(pk=2))
	
	dias = []
	
	for num in entorno.DIAS:
		if num in entorno.espacio.dias_habiles:
			dias.append(entorno.DIAS[num])
	
	context = {'entorno': entorno, 'dias': dias}
	
	return render(request, 'calendario/add.html', context)

def generar(request):
	
	start_time = time.time()
	
	espacio = Espacio.objects.get(pk=2)
	
	entorno = Entorno(espacio=espacio)
	
	entorno.generar_poblacion_inicial()
	
	entorno.evolucionar()
	
	tiempo = (time.time() - start_time)
	
	context = {'calendarios': entorno.poblacion, 'tiempo': tiempo, 'cantidad': len(entorno.poblacion)}
	
	return render(request, 'calendario/all.html', context)

def detail(request, calendario_id):
	
	calendario = get_object_or_404(Calendario, pk=calendario_id)
	
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

def profesional_all(request):
	
	profesionales = Profesional.objects.all().order_by('apellido', 'nombre')
	
	context = {'profesionales': profesionales, }
	
	return render(request, 'calendario/profesional/all.html', context)

def profesional_add(request):
	
	context = {}
	
	if request.method == 'POST':
		
		try:
			profesional = Profesional()
			
			profesional.nombre = request.POST["nombre"]
			profesional.apellido = request.POST["apellido"]
			profesional.cuil = request.POST["cuil"]
			profesional.especialidad = Especialidad.objects.get(pk=request.POST["especialidad"])
			
			profesional.save()
			
			return HttpResponseRedirect(reverse('calendario:profesional_all'))
			
		except Exception as ex:
			context['error_message'] = "Error al guardar el profesional: " + str(ex)
	
	especialidades = Especialidad.objects.all().order_by('nombre')
	
	context['especialidades'] = especialidades
	
	return render(request, 'calendario/profesional/add.html', context)

def profesional_edit(request, profesional_id):
	
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
	
	return render(request, 'calendario/profesional/edit.html', context)

def profesional_delete(request, profesional_id):
	
	if request.method == 'POST':
		
		context = {}
		
		try:
			profesional = Profesional.objects.get(pk=profesional_id)
			
			profesional.delete()
			
			return HttpResponseRedirect(reverse('calendario:profesional_all'))
			
		except Exception as ex:
			context['error_message'] = "Error eliminando el profesional: " + str(ex)
		
		return render(request, 'calendario/profesional/all.html', context)
	
	return HttpResponseRedirect(reverse('calendario:profesional_all'))

def especialidad_all(request):
	
	especialidades = Especialidad.objects.all().order_by('nombre')
	
	context = {'especialidades' : especialidades}
	
	return render(request, 'calendario/especialidad/all.html', context)

def especialidad_add(request):
	
	context = {}
	
	if request.method == 'POST':
		
		try:
			especialidad = Especialidad()
			
			especialidad.nombre = request.POST["nombre"]
			especialidad.carga_horaria_semanal = request.POST["carga_horaria_semanal"]
			especialidad.max_horas_diaria = request.POST["max_horas_diaria"]
			
			especialidad.save()
			
			return HttpResponseRedirect(reverse('calendario:especialidad_all'))
			
		except Exception as ex:
			context['error_message'] = "Error al guardar la especialidad: " + str(ex)
	
	return render(request, 'calendario/especialidad/add.html', context)

def especialidad_edit(request, especialidad_id):
	
	context = {}
	
	especialidad = Especialidad.objects.get(pk=especialidad_id)
	
	if request.method == 'POST':
		
		try:
			especialidad.nombre = request.POST["nombre"]
			especialidad.carga_horaria_semanal = request.POST["carga_horaria_semanal"]
			especialidad.max_horas_diaria = request.POST["max_horas_diaria"]
			
			especialidad.save()
			
			return HttpResponseRedirect(reverse('calendario:especialidad_all'))
			
		except Exception as ex:
			context['error_message'] = "Error editando la especialidad: " + str(ex)
	
	context['especialidad'] = especialidad
	
	return render(request, 'calendario/especialidad/edit.html', context)

def especialidad_delete(request, especialidad_id):
	
	if request.method == 'POST':
		
		context = {}
		
		try:
			especialidad = Especialidad.objects.get(pk=especialidad_id)
			
			especialidad.delete()
			
			return HttpResponseRedirect(reverse('calendario:especialidad_all'))
			
		except Exception as ex:
			context['error_message'] = "Error eliminando la especialidad: " + str(ex)
		
		return render(request, 'calendario/especialidad/all.html', context)
	
	return HttpResponseRedirect(reverse('calendario:especialidad_all'))
