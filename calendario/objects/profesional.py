# -*- coding: utf-8 -*-
from django.db import models
from persona import Persona
from especialidad import Especialidad

class Profesional(Persona):
	
	restricciones = []
	especialidades = models.ManyToManyField(Especialidad)
	
	def __str__(self, ):
		return self.apellido.encode('utf-8') + ", " + self.nombre.encode('utf-8')
	
	def __eq__(self, o):
		return self.cuil == o.cuil
