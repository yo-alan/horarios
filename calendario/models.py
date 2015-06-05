from django.db import models


class Profesional(models.Model):
	
	nombre = models.CharField(max_length=100, blank=True)
	apellido = models.CharField(max_length=100, blank=True)
	cuil = models.IntegerField(default=0, blank=True)
	especialidad = models.CharField(max_length=100, blank=True)
	
	def __str__(self, ):
		return self.apellido + ", " + self.nombre

class Calendario(models.Model):
	
	curso = models.CharField(max_length=100, blank=True)
	horarios = [[], [], [], [], [], [], [], [], []]
	puntaje = models.IntegerField(default=0)
	ranking_distribucion = models.FloatField(default=100)
	

class Horario(models.Model):
	
	id_profesional = models.ForeignKey(Profesional, blank=True)
	hora_desde = models.TimeField('desde', blank=True)
	hora_hasta = models.TimeField('hasta', blank=True)
	dia_semana = models.IntegerField(default=0, blank=True)
	id_calendario = models.ForeignKey(Calendario, blank=False)
	
	def __eq__(self, o):
		return hora_desde == o._hora_desde and hora_hasta == o._hora_hasta and dia_semana == o._dia_semana
	

class Restriccion(models.Model):
	
	hora_desde = models.TimeField('desde', blank=True)
	hora_hasta = models.TimeField('hasta', blank=True)
	dia_semana = models.IntegerField(default=0, blank=True)
	

class Espacio(models.Model):
	pass
	

class Materia(models.Model):
	
	nombre = models.CharField(max_length=100, blank=True)
	carga_horaria_semanal = models.IntegerField(default=0, blank=True)
	restriccion_diaria = models.IntegerField(default=0, blank=True)
	
	
