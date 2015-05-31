import random, time

from django.shortcuts import render
from django.http import HttpResponse

from .models import Calendario, Profesional, Horario, Restriccion

dias = {0 : "Domingo", 1 : "Lunes", 2 : "Martes", 3 : "Miercoles", 4 : "Jueves", 5 : "Viernes", 6 : "Sabado"}
horarios = {1 : "7:30", 2 : "8:10", 3 : "8:50", 4 : "9:00", 5 : "9:40", 6 : "10:30", 7 : "11:10", 8 : "11:50"}

#RESQUESTS

def index(request):
	ps = []
	
	#~ p = Profesional()
	#~ p.nombre = "Pedro"
	#~ p.apellido = "Perez"
	#~ p.especialidad = "Prof. Matematica"
	#~ p.documento = 30000000
	#~ 
	#~ ps.append(p)
	#~ 
	#~ p = Profesional()
	#~ p.nombre = "Rodrigo"
	#~ p.apellido = "Rodriguez"
	#~ p.especialidad = "Prof. Lengua"
	#~ p.documento = 31000000
	#~ 
	#~ ps.append(p)
	#~ 
	#~ p = Profesional()
	#~ p.nombre = "Gonzalo"
	#~ p.apellido = "Gonzalez"
	#~ p.especialidad = "Prof. Historia"
	#~ p.documento = 32000000
	#~ 
	#~ ps.append(p)
	#~ 
	start_time = time.time()
	
	ps = Profesional.objects.all()
	
	hs = generar_poblacion(ps)
	
	cs = [] #La poblacion de calendarios
	
	i = 1
	for h in hs:
		
		c = Calendario(curso="1ro 1ra")
		c.save()
		c.horarios.append(h)
		h.id_calendario = c
		h.save()
		cs.append(c)
		
		i = i + 1
		
	
	total_horarios = len(dias) * (len(horarios) - 1)
	objetos_i = 0
	objetos_n = 0
	for c in cs:
		
		while len(c.horarios) < total_horarios:
			
			desde = random.randrange(1, 8)
			
			h = Horario(id_profesional=random.randrange(1, 4), hora_desde=horarios[desde], hora_hasta=horarios[desde + 1], dia_semana=random.randrange(1, 6), id_calendario=c.id)
			
			if h not in c.horarios:
				c.horarios.append(h)
				objetos_n = objetos_n + 1
				h.save()
			else:
				objetos_i = objetos_i + 1
	
	tiempo = (time.time() - start_time)
	context = {'cs': cs, 'tiempo' : tiempo}
	
	return render(request, 'calendario/index.html', context)


def detail(request, calendario_id):
	return HttpResponse("Estas viendo el calendario %s." % calendario_id)


#FIN RESQUESTS

def generar_poblacion(ps):

	hs = []

	l = 1
	for i in range(1, 6):
		for j in range(1, 8):
			for k in ps:
				h = Horario()
				h.id_profesional = Profesional.objects.get(pk=k.id)
				h.hora_desde = horarios[j]
				h.hora_hasta = horarios[j+1]
				h.dia_semana = i
				h.save()
				
				hs.append(h)
				
				l = l + 1

	return hs
