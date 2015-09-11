# -*- coding: utf-8 -*-
from django.db import models

from restriccion import Restriccion
from profesional import Profesional

class ProfesionalRestriccion(Restriccion):
	
	profesional = models.ForeignKey(Profesional)
	
	def setprofesional(self, profesional):
		
		self.profesional = profesional
	
	def setdia_semana(self, dia_semana):
		
		self.dia_semana = dia_semana
	
	def sethora_desde(self, hora_desde):
		
		self.hora_desde = hora_desde
	
	def sethora_hasta(self, hora_hasta):
		
		self.hora_hasta = hora_hasta
	
