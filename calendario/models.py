from django.db import models


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
	horarios = [[], [], [], [], [], [], []]
	puntaje = models.IntegerField(default=0)
	ranking_distribucion = models.FloatField(default=100)
	
	def getHorarios(self, ):
		
		hs = Horario.objects.filter(calendario=self).order_by('hora_desde')
		
		self.horarios = [[], [], [], [], [], [], []]
		
		for h in hs:
			self.horarios[h.dia_semana].append(h)
		
		return self.horarios
	
	def cruce(self, madre):
		pass
	

class Horario(models.Model):
	
	profesional = models.ForeignKey(Profesional, blank=True)
	hora_desde = models.TimeField('desde', blank=True)
	hora_hasta = models.TimeField('hasta', blank=True)
	dia_semana = models.IntegerField(default=0, blank=True)
	calendario = models.ForeignKey(Calendario, null=False)
	
	def __str__(self, ):
		return str(self.profesional.especialidad)
	
	def __eq__(self, o):
		return self.hora_desde == o.hora_desde and self.hora_hasta == o.hora_hasta and self.dia_semana == o.dia_semana
	

class Restriccion(models.Model):
	
	hora_desde = models.TimeField('desde', blank=True)
	hora_hasta = models.TimeField('hasta', blank=True)
	dia_semana = models.IntegerField(default=0, blank=True)
	#FALTA TERMINAR DE DEFINIRLO
	
	def __eq__(self, o):
		pass
		#return self.hora_desde == o.hora_desde and self.hora_hasta == o.hora_hasta and self.
	

class Espacio(models.Model):
	pass
	

class Ecosistema(object):
	
	poblacion = []
	restricciones = []
	generaciones = 0
	
	def __init__(self, rs, generaciones=50):
		self.restricciones = rs
		self.generaciones = generaciones
	
	def generar_poblacion_inicial(self, ):
		pass
	
	def evolucionar(self, ):
		pass
	
	def evaluar(self, c):
		
		if not isinstance(c, Calendario):
			raise Exception("No puedo evaluar algo que no sea un Calendario.")
		
		aptitud_val = 0
		
		#TO DO
		
		return aptitud_val
	
	def seleccionar(self, ):
		pass
	
	
	
