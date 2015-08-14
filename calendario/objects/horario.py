# -*- coding: utf-8 -*-
from django.db import models
from calendario import Calendario
from especialidad import Especialidad

class Horario(models.Model):
	
	hora_desde = models.TimeField('desde', null=False)
	hora_hasta = models.TimeField('hasta', null=False)
	dia_semana = models.IntegerField(default=0, null=False)
	calendario = models.ForeignKey(Calendario, null=True)
	especialidad = models.ForeignKey(Especialidad)
	
	def __str__(self, ):
		return str(self.especialidad)
	
	def __eq__(self, o):
		return self.hora_desde == o.hora_desde and\
				self.hora_hasta == o.hora_hasta and\
				self.dia_semana == o.dia_semana and\
				self.calendario == o.calendario
	
	def __ne__(self, o):
		return self.dia_semana != o.dia_semana and self.hora_desde != o.hora_desde
	
	def __lt__(self, o):
		if self.dia_semana == o.dia_semana:
			return self.hora_desde < o.hora_desde
		
		return self.dia_semana < o.dia_semana
	
	def __le__(self, o):
		if self.dia_semana == o.dia_semana:
			return self.hora_desde <= o.hora_desde
		
		return self.dia_semana <= o.dia_semana
	
	def __gt__(self, o):
		if self.dia_semana == o.dia_semana:
			return self.hora_desde > o.hora_desde
		
		return self.dia_semana > o.dia_semana
	
	def __ge__(self, o):
		if self.dia_semana == o.dia_semana:
			return self.hora_desde >= o.hora_desde
		
		return self.dia_semana >= o.dia_semana
