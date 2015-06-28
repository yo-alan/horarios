from random import random, randrange
from django.db import models


DIAS = {0 : "Domingo", 1 : "Lunes", 2 : "Martes", 3 : "Miercoles", 4 : "Jueves", 5 : "Viernes", 6 : "Sabado"}
#HARDCODED
horarios = {1 : "7:30", 2 : "8:10", 3 : "9:00", 4 : "9:40", 5 : "10:30", 6 : "11:10", 7 : "11:50"}

class Especialidad(models.Model):
	
	nombre = models.CharField(max_length=100, null=False)
	carga_horaria_semanal = models.IntegerField(default=0, null=False)
	max_horas_diaria = models.IntegerField(default=0, null=False)
	
	def __str__(self, ):
		return self.nombre
	
	def __eq__(self, o):
		return self.nombre == o.nombre
	

class Espacio(models.Model):
	
	nombre = models.CharField(max_length=100, null=False, blank=False)
	
	def __str__(self, ):
		return self.nombre

class Persona(models.Model):
	
	nombre = models.CharField(max_length=100, null=False, blank=False)
	apellido = models.CharField(max_length=100, null=False, blank=False)
	cuil = models.CharField(max_length=11, unique=True, null=False, blank=False)

class Profesional(Persona):
	
	restricciones = []
	especialidad = models.ForeignKey(Especialidad)
	
	def __str__(self, ):
		return self.apellido + ", " + self.nombre
	
	def __eq__(self, o):
		return self.cuil == o.cuil

class Calendario(models.Model):
	
	espacio = models.ForeignKey(Espacio)
	horarios = []
	puntaje = models.IntegerField(default=0)
	
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
	
	def cruce(self, madre, prob_mutacion=0.01):
		
		if not isinstance(madre, Calendario):
			raise Exception("El objeto no es de tipo Calendario.")
		
		if self == madre:
			raise Exception("Un Calendario no puede cruzarse consigo mismo.")
		
		
		
	
	def mutar(self, ):
		pass
	

class Horario(models.Model):
	
	hora_desde = models.TimeField('desde', null=False)
	hora_hasta = models.TimeField('hasta', null=False)
	dia_semana = models.IntegerField(default=0, null=False)
	calendario = models.ForeignKey(Calendario)
	profesional = models.ForeignKey(Profesional)
	
	def __str__(self, ):
		#~ return str(self.profesional.especialidad)
		return str(self.hora_desde)
	
	def __eq__(self, o):
		return self.hora_desde == o.hora_desde and self.hora_hasta == o.hora_hasta and self.dia_semana == o.dia_semana and self.calendario == o.calendario
	

class Restriccion(models.Model):
	
	hora_desde = models.TimeField('desde', null=False, blank=False)
	hora_hasta = models.TimeField('hasta', null=False, blank=False)
	dia_semana = models.IntegerField(default=0, null=False, blank=False)
	
	def __eq__(self, o):
		pass
		#return self.hora_desde == o.hora_desde and self.hora_hasta == o.hora_hasta and self.

class Espacio_restriccion(Restriccion):
	
	espacio = models.ForeignKey(Espacio)

class Profesional_restriccion(Restriccion):
	
	profesional = models.ForeignKey(Profesional)

class Entorno(object):
	
	poblacion = []
	restricciones = []
	generaciones = 0
	espacio = None
	
	def __init__(self, generaciones=50, espacio=None):
		self.restricciones = Restriccion.objects.all()
		self.generaciones = generaciones
		self.espacio = espacio
		
		self.generar_poblacion_inicial()
	
	def generar_poblacion_inicial(self, ):
		
		ps = Profesional.objects.all()
		
		#DETERMINAMOS TODAS LAS POSIBLES COMBINACIONES DE HORARIOS
		#HARDCODED
		for i in range(1, 6):
			for j in range(1, len(horarios)):
				for k in ps:
					c = Calendario()
					c.espacio = self.espacio
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
					
					h = Horario(profesional=ps[randrange(1, len(ps))], hora_desde=horarios[horario], hora_hasta=horarios[horario+1], dia_semana=dia, calendario=c)
					
					existe = False
					for dh in c.horarios:
						for hh in dh:
							if h == hh:
								existe = True
					
					if existe:
						continue
					
					h.save()
					
					c.agregar_horario(h)
		
	
	def evolucionar(self, ):
		pass
	
	def fitness(self, ):
		
		for c in self.poblacion:
			
			if c.puntaje != 0:
				continue
			
			for h in c:
				for r in rs:
					if (h.desde >= r.desde and h.desde <= r.hasta) or \
						(h.hasta >= r.desde and h.hasta <= r.hasta) or \
						(h.desde <= r.desde and h.hasta >= r.hasta):#OJOOOOOOO h.desde <= r.desde???
						c.puntaje += 1
						
		
		es = Especialidad.objects.all()
		
		for c in cs:
			
			for e in es:
				
				horas_semanales = 0
				for i in range(0, 6):
					
					for h in c.horarios[i]:
						
						if h.profesional.especialidad == e:
							horas_semanales += 1
					
					if horas_semanales != e.carga_horaria_semanal:
						#-20% (del ranking)
						x = abs(e.carga_semanal - contador)
						#HARDCODED
						y = (35 - e.carga_semanal) / (x * 100)
						#HARDCODED
						p_total += (100 / len(especialidad) / (20 + y) * 100)
		
		return aptitud_val
	
	def seleccionar(self, ):
		pass
	
	
	
