import time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Entorno, Calendario, Profesional, Horario, Restriccion, Especialidad, Espacio


def index(request):
	
	context = {}
	
	return render(request, 'calendario/index.html', context)

def all(request):
	
	cs = Calendario.objects.all()
	
	context = {'cs': cs, 'cantidad': len(cs)}
	
	return render(request, 'calendario/all.html', context)

def generar(request):
	
	start_time = time.time()
	
	espacio = Espacio.objects.get(pk=1)
	
	e = Entorno(espacio=espacio)
	
	e.evolucionar()
	
	tiempo = (time.time() - start_time)
	
	context = {'cs': e.poblacion, 'tiempo' : tiempo}
	
	return render(request, 'calendario/all.html', context)

def detail(request, calendario_id):
	
	calendario = get_object_or_404(Calendario, pk=calendario_id)
	
	context = {'calendario': calendario, 'dias' : range(5), 'horas' : range(6)}
	
	return render(request, 'calendario/detail.html', context)

def profesional_all(request):
	
	ps = Profesional.objects.all().order_by('apellido', 'nombre')
	
	context = {'ps': ps, }
	
	return render(request, 'calendario/profesional/all.html', context)

def profesional_add(request):
	
	context = {}
	
	if request.method == 'POST':
		
		try:
			p = Profesional()
			
			p.nombre = request.POST["nombre"]
			p.apellido = request.POST["apellido"]
			p.cuil = request.POST["cuil"]
			p.especialidad = Especialidad.objects.get(pk=request.POST["especialidad"])
			
			p.save()
			
			return HttpResponseRedirect(reverse('calendario:profesional_all'))
			
		except Exception as ex:
			context['error_message'] = "Error al guardar el profesional: " + str(ex)
	
	es = Especialidad.objects.all().order_by('nombre')
	
	context['es'] = es
	
	return render(request, 'calendario/profesional/add.html', context)

def profesional_edit(request, profesional_id):
	
	context = {}
	
	p = Profesional.objects.get(pk=profesional_id)
	
	if request.method == 'POST':
		
		try:
			p.nombre = request.POST["nombre"]
			p.apellido = request.POST["apellido"]
			p.cuil = request.POST["cuil"]
			p.especialidad = Especialidad.objects.get(pk=request.POST["especialidad"])
			
			p.save()
			
			return HttpResponseRedirect(reverse('calendario:profesional_all'))
			
		except Exception as ex:
			context['error_message'] = "Error editando el profesional: " + str(ex)
	
	es = Especialidad.objects.all().order_by('nombre')
	
	context['p'] = p
	context['es'] = es
	
	return render(request, 'calendario/profesional/edit.html', context)

def especialidad_all(request):
	
	es = Especialidad.objects.all().order_by('nombre')
	
	context = {'es' : es}
	
	return render(request, 'calendario/especialidad/all.html', context)

def especialidad_add(request):
	
	context = {}
	
	if request.method == 'POST':
		
		try:
			e = Especialidad()
			
			e.nombre = request.POST["nombre"]
			e.carga_horaria_semanal = request.POST["carga_horaria_semanal"]
			e.max_horas_diaria = request.POST["max_horas_diaria"]
			
			e.save()
			
			return HttpResponseRedirect(reverse('calendario:especialidad_all'))
			
		except Exception as ex:
			context['error_message'] = "Error al guardar la especialidad: " + str(ex)
	
	return render(request, 'calendario/especialidad/add.html', context)

def especialidad_edit(request, especialidad_id):
	
	context = {}
	
	e = Especialidad.objects.get(pk=especialidad_id)
	
	if request.method == 'POST':
		
		try:
			e.nombre = request.POST["nombre"]
			e.carga_horaria_semanal = request.POST["carga_horaria_semanal"]
			e.max_horas_diaria = request.POST["max_horas_diaria"]
			
			e.save()
			
			return HttpResponseRedirect(reverse('calendario:profesional_all'))
			
		except Exception as ex:
			context['error_message'] = "Error editando la especialidad: " + str(ex)
	
	context['e'] = e
	
	return render(request, 'calendario/especialidad/edit.html', context)
