import random

from django.db import models


dias = {0 : "Domingo", 1 : "Lunes", 2 : "Martes", 3 : "Miercoles", 4 : "Jueves", 5 : "Viernes", 6 : "Sabado"}
#HARDCODED
horarios = {1 : "7:30", 2 : "8:10", 3 : "9:00", 4 : "9:40", 5 : "10:30", 6 : "11:10", 7 : "11:50"}

class Especialidad(models.Model):
	
	nombre = models.CharField(max_length=100, blank=True)
	carga_horaria_semanal = models.IntegerField(default=0, blank=True)
	restriccion_diaria = models.IntegerField(default=0, blank=True)
	
	def __str__(self, ):
		return self.nombre
	
	def __eq__(self, o):
		return self.nombre == o.nombre
	

class Profesional(models.Model):
	
	nombre = models.CharField(max_length=100, blank=True)
	apellido = models.CharField(max_length=100, blank=True)
	cuil = models.CharField(max_length=11, blank=True, unique=True, null=False)
	especialidad = models.ForeignKey(Especialidad)
	
	def __str__(self, ):
		return self.apellido + ", " + self.nombre
	
	def __eq__(self, o):
		return self.cuil == o.cuil

class Calendario(models.Model):
	
	nombre = models.CharField(max_length=100, blank=True)
	horarios = []
	puntaje = models.IntegerField(default=0)
	ranking_distribucion = models.FloatField(default=100)
	
	def getHorarios(self, ):
		
		hs = Horario.objects.filter(calendario=self).order_by('hora_desde', 'dia_semana')
		
		self.horarios = []
		
		for h in hs:
			self.agregar_horario(h)
		
		return self.horarios
	
	def agregar_horario(self, horario):
		
		if self.horarios == []:
			self.horarios.append([horario])
			return
		
		for hs in self.horarios:
			if hs[0].hora_desde == horario.hora_desde:
				hs.append(horario)
				return
		
		self.horarios.append([horario])
	
	def cruce(self, madre):
		pass
	

class Horario(models.Model):
	
	profesional = models.ForeignKey(Profesional, blank=True)
	hora_desde = models.TimeField('desde', blank=True)
	hora_hasta = models.TimeField('hasta', blank=True)
	dia_semana = models.IntegerField(default=0, blank=True)
	calendario = models.ForeignKey(Calendario, null=False)
	
	def __str__(self, ):
		#~ return str(self.profesional.especialidad)
		return str(self.hora_desde)
	
	def __eq__(self, o):
		return self.hora_desde == o.hora_desde and self.hora_hasta == o.hora_hasta and self.dia_semana == o.dia_semana and self.calendario == o.calendario
	

class Restriccion(models.Model):
	
	hora_desde = models.TimeField('desde', blank=True)
	hora_hasta = models.TimeField('hasta', blank=True)
	dia_semana = models.IntegerField(default=0, blank=True)
	#FALTA TERMINAR DE DEFINIRLO UNA RESTRICCION GENERICAS, PARA ESPACIO Y PROF
	
	def __eq__(self, o):
		pass
		#return self.hora_desde == o.hora_desde and self.hora_hasta == o.hora_hasta and self.
	

class Espacio(models.Model):
	pass
	

class Ecosistema(object):
	
	poblacion = []
	restricciones = []
	generaciones = 0
	
	def __init__(self, generaciones=50):
		self.restricciones = Restriccion.objects.all()
		self.generaciones = generaciones
	
	def generar_poblacion_inicial(self, ):
		
		ps = Profesional.objects.all()
		
		#DETERMINAMOS TODAS LAS POSIBLES COMBINACIONES DE HORARIOS
		#HARDCODED
		for i in range(1, 6):
			for j in range(1, len(horarios)):
				for k in ps:
					c = Calendario()
					c.save()
					h = Horario()
					h.profesional = Profesional.objects.get(pk=k.id)
					h.hora_desde = horarios[j]
					h.hora_hasta = horarios[j+1]
					h.dia_semana = i
					h.calendario = c
					h.save()
					
					c.agregar_horario(h)
					
					self.poblacion.append(c)
					
		
		#LLENAMOS LOS CALENDARIOS CON LOS HORARIOS FALTANTES
		for c in self.poblacion:
			
			#HARDCODED
			for dia in range(1, 6):
				
				for horario in range(1, len(horarios)):
					
					h = Horario(profesional=ps[random.randrange(1, len(ps))], hora_desde=horarios[horario], hora_hasta=horarios[horario+1], dia_semana=dia, calendario=c)
					
					existe = False
					for dh in c.horarios:
						for hh in dh:
							if h == hh:
								print str(h.hora_desde) + " == " + str(hh.hora_desde)
								print str(h.hora_hasta) + " == " + str(hh.hora_hasta)
								print str(h.dia_semana) + " == " + str(hh.dia_semana)
								existe = True
					
					if existe:
						continue
					
					h.save()
					
					c.agregar_horario(h)
		
	
	def evolucionar(self, ):
		pass
	
	def evaluar(self, c):
		
		if not isinstance(c, Calendario):
			raise Exception("No puedo evaluar algo que no sea un Calendario.")
		
		aptitud_val = 0
		
		#PREGUNTAR SI SE EVALUAN INDIVIDUALMENTE O TODA LA POBLACION
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
		
		return aptitud_val
	
	def seleccionar(self, ):
		pass
	
	
	
