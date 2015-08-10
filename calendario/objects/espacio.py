# -*- coding: utf-8 -*-
from django.db import models

class Espacio(models.Model):
	
	nombre = models.CharField(max_length=100, null=False, blank=False)
	
	@classmethod
	def create(cls, espacio_id=0):
		
		espacio = None
		
		if espacio_id != 0:
			espacio = Espacio.objects.get(pk=espacio_id)
		else:
			espacio = Espacio()
		
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
	def especialidades(self, ):
		return []
