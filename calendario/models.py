from django.db import models


class Horario(models.Model):
	
	def __init__(self):
		id_profesional = models.ForeignKey(Profesional, blank=True)
		hora_desde = models.TimeField('desde', blank=True)
		hora_hasta = models.TimeField('hasta', blank=True)
		dia_semana = models.IntegerField(default=0, blank=True)
		id_calendario = models.ForeignKey(Calendario)
	
	def __eq__(self, o):
		return hora_desde == o._hora_desde and hora_hasta == o._hora_hasta and dia_semana == o._dia_semana
	

class Profesional(models.Model):
	
	def __init__(self):
		nombre = models.CharField(max_length=100, blank=True)
		apellido = models.CharField(max_length=100, blank=True)
		documento = models.IntegerField(default=0, blank=True)
		especialidad = models.CharField(max_length=100, blank=True)
	

class Restriccion(models.Model):
	
	def __init__(self):
		hora_desde = models.TimeField('desde', blank=True)
		hora_hasta = models.TimeField('hasta', blank=True)
		dia_semana = models.IntegerField(default=0, blank=True)
	

class Calendario(models.Model):
	
	def __init__(self):
		curso = models.CharField(max_length=100, blank=True)
		horarios = []#ACA ESTA EL PROBLEMA
		puntaje = models.IntegerField(default=0)
		ranking_distribucion = models.FloatField(default=100)
	

class Espacio(models.Model):
	
	def __init__(self):
		pass
	

