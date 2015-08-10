# -*- coding: utf-8 -*-
from django.db import models

class Restriccion(models.Model):
	
	hora_desde = models.TimeField('desde', null=False, blank=False)
	hora_hasta = models.TimeField('hasta', null=False, blank=False)
	dia_semana = models.IntegerField(default=0, null=False, blank=False)
	
	def __eq__(self, o):
		pass
		#return self.hora_desde == o.hora_desde and self.hora_hasta == o.hora_hasta and self.
