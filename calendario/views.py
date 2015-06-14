import time

from django.shortcuts import render, get_object_or_404

from .models import Ecosistema, Calendario, Profesional, Horario, Restriccion, Especialidad


def index(request):
	
	context = {}
	
	return render(request, 'calendario/index.html', context)

def all(request):
	
	start_time = time.time()
	
	e = Ecosistema()
	
	e.generar_poblacion_inicial()
	
	
	tiempo = (time.time() - start_time)
	
	context = {'cs': e.poblacion, 'tiempo' : tiempo}
	
	return render(request, 'calendario/all.html', context)

def detail(request, calendario_id):
	
	calendario = get_object_or_404(Calendario, pk=calendario_id)
	
	return render(request, 'calendario/detail.html', {'calendario': calendario, 'dias' : range(5), 'horas' : range(6)})
