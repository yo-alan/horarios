# -*- coding: utf-8 -*-
from random import random, randrange

from django.db import models

from espacio import Espacio
from especialidad import Especialidad
from profesional import Profesional

class Coordinador(models.Model):
	"""
	DEFINICION.
	
	@Atributos:
	.espacio - .
	.especialidad - .
	.profesional - .
	"""
	
	espacio = models.ForeignKey(Espacio)
	especialidad = models.ForeignKey(Especialidad)
	profesional = models.ForeignKey(Profesional)
	
