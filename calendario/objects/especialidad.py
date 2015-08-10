# -*- coding: utf-8 -*-
from django.db import models
from espacio import Espacio

class Especialidad(models.Model):
	
	nombre = models.CharField(max_length=100, null=False)
	carga_horaria_semanal = models.IntegerField(default=0, null=False)
	max_horas_diaria = models.IntegerField(default=0, null=False)
	espacios = models.ManyToManyField(Espacio)
	
	def __str__(self, ):
		return unicode(self.nombre).encode('utf-8')
	
	def __eq__(self, o):
		return self.nombre == o.nombre	
