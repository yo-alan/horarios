# -*- coding: utf-8 -*-
from django.db import models
from especialidad import Especialidad

class Espacio(models.Model):
	
	nombre = models.CharField(max_length=100, null=False, blank=False)
	estado = models.CharField(max_length=3, choices=[('ON', 'ON'), ('OFF', 'OFF')], default='ON')
	usuario_creador = models.CharField(max_length=30, default='admin')
	fecha_creacion = models.DateField(auto_now_add=True)
	usuario_modificador = models.CharField(max_length=30, default='admin')
	fecha_modificacion = models.DateField(auto_now=True)
	
	especialidades = models.ManyToManyField(Especialidad)
	
	@classmethod
	def create(cls, espacio_id=0):
		
		espacio = None
		
		if espacio_id != 0:
			espacio = Espacio.objects.get(pk=espacio_id)
		else:
			espacio = Espacio()
		
		espacio._calendarios = []
		espacio._horas = []
		#HARDACODED
		espacio._dias_habiles = [1, 2, 3, 4, 5]
		
		return espacio
	
	def __str__(self, ):
		return self.nombre.encode('utf-8')
	
	@property
	def horas(self, ):
		from hora import Hora
		
		if not self._horas:
			self._horas = Hora.objects.filter(espacio=self).order_by('hora_desde')
		
		return self._horas
	
	@property
	def dias_habiles(self, ):
		return self._dias_habiles
	
	@property
	def calendarios(self, ):
		from calendario import Calendario
		
		if not self._calendarios:
			self._calendarios = Calendario.objects.filter(espacio=self)
		
		return self._calendarios
	
	def setnombre(self, nombre):
		
		if nombre == "":
			raise Exception("El nombre no puede estar vacío.")
		
		self.nombre = nombre
	
