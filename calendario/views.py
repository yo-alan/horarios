import random, time

from django.shortcuts import render, get_object_or_404

from .models import Calendario, Profesional, Horario, Restriccion, Especialidad


dias = {0 : "Domingo", 1 : "Lunes", 2 : "Martes", 3 : "Miercoles", 4 : "Jueves", 5 : "Viernes", 6 : "Sabado"}
#HARDCODED
horarios = {1 : "7:30", 2 : "8:10", 3 : "9:00", 4 : "9:40", 5 : "10:30", 6 : "11:10", 7 : "11:50"}

#RESQUESTS

def index(request):
	
	start_time = time.time()
	
	ps = Profesional.objects.all()
	
	hs = generar_horarios(ps)
	
	cs = [] #La poblacion de calendarios
	
	for h in hs:
		
		c = Calendario()
		c.save()
		c.horarios.append(h)
		h.calendario = c
		h.save()
		cs.append(c)
	
	for c in cs:
		
		#HARDCODED
		for dia in range(1, 6):
			
			for horario in range(1, len(horarios)):
				
				h = Horario(profesional=ps[random.randrange(1, len(ps))], hora_desde=horarios[horario], hora_hasta=horarios[horario+1], dia_semana=dia, calendario=c)
				
				#if h not in c.horarios[h.dia_semana]:
					
				h.save()
				
				c.horarios[h.dia_semana].append(h)
	
	
	tiempo = (time.time() - start_time)
	context = {'cs': cs, 'tiempo' : tiempo, 'dias' : range(5), 'horas' : range(6)}
	
	return render(request, 'calendario/index.html', context)


def detail(request, calendario_id):
	
	calendario = get_object_or_404(Calendario, pk=calendario_id)
	
	return render(request, 'calendario/detail.html', {'calendario': calendario})


#FIN RESQUESTS

def generar_horarios(ps):

	hs = []

	l = 1
	for i in range(1, 6):
		for j in range(1, len(horarios)):
			for k in ps:
				h = Horario()
				h.profesional = Profesional.objects.get(pk=k.id)
				h.hora_desde = horarios[j]
				h.hora_hasta = horarios[j+1]
				h.dia_semana = i
				h.save()
				
				hs.append(h)
				
				l = l + 1

	return hs

def aptitud(cs):
	
	rs = Restriccion.objects.all()
	
	for c in cs:
		
		for h in c:
			
			for r in rs:
				
				if (h.desde >= r.desde and h.desde <= r.hasta) or \
					(h.hasta >= r.desde and h.hasta <= r.hasta) or \
					(h.desde <= r.desde and h.hasta >= r.hasta):#OJOOOOOOO h.desde <= r.desde???
					c.puntaje = c.puntaje + 1
					
	
	es = Especialidad.objects.all()
	
	for c in cs:
		
		for e in es: #e = especializacion , es = especializaciones
			
			horas_semanales = 0
			for i in range(0, 6):
				
				for h in c.horarios[i]:
					
					if h.profesional.especialidad == e:
						horas_semanales = horas_semanales + 1
				
				if horas_semanales != e.carga_horaria_semanal:
					#-20% (del ranking)
					x = abs(e.carga_semanal - contador)
					#HARDCODED
					y = (35 - e.carga_semanal) / (x * 100)
					#HARDCODED
					p_total = p_total + (100 / len(especialidad) / (20 + y) * 100)
