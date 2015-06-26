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
	
	context = {'cs': cs, }
	
	return render(request, 'calendario/all.html', context)

def generar(request):
	
	start_time = time.time()
	
	espacio = Espacio.objects.get(pk=1)
	
	e = Entorno(espacio=espacio)
	
	
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
			context['error_message'] = "Ocurrio un error al guardar el profesional: " + str(ex)
	
	es = Especialidad.objects.all()
	
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
			context['error_message'] = "Ocurrio un error editando el profesional: " + str(ex)
	
	es = Especialidad.objects.all()
	
	context = {'p': p, 'es' : es}
	
	return render(request, 'calendario/profesional/edit.html', context)
