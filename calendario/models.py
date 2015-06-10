from django.db import models


class Especialidad(models.Model):
	
	nombre = models.CharField(max_length=100, blank=True)
	carga_horaria_semanal = models.IntegerField(default=0, blank=True)
	restriccion_diaria = models.IntegerField(default=0, blank=True)
	
	def __str__(self, ):
		return self.nombre
	

class Profesional(models.Model):
	
	nombre = models.CharField(max_length=100, blank=True)
	apellido = models.CharField(max_length=100, blank=True)
	cuil = models.CharField(max_length=11, blank=True)
	especialidad = models.ForeignKey(Especialidad)
	
	def __str__(self, ):
		return self.apellido + ", " + self.nombre

class Calendario(models.Model):
	
	nombre = models.CharField(max_length=100, blank=True)
	horarios = [[], [], [], [], [], [], []]
	puntaje = models.IntegerField(default=0)
	ranking_distribucion = models.FloatField(default=100)
	
	def getHorarios(self, ):
		
		hs = Horario.objects.filter(calendario=self).order_by('hora_desde')
		
		self.horarios = [[], [], [], [], [], [], []]
		
		for h in hs:
			self.horarios[h.dia_semana].append(h)
		
		return self.horarios

class Horario(models.Model):
	
	profesional = models.ForeignKey(Profesional, blank=True)
	hora_desde = models.TimeField('desde', blank=True)
	hora_hasta = models.TimeField('hasta', blank=True)
	dia_semana = models.IntegerField(default=0, blank=True)
	calendario = models.ForeignKey(Calendario, null=False)
	
	def __str__(self, ):
		return str(self.profesional.especialidad)
	
	def __eq__(self, o):
		return self.hora_desde == o.hora_desde and self.hora_hasta == o.hora_hasta and self.dia_semana == o.dia_semana
	

class Restriccion(models.Model):
	
	hora_desde = models.TimeField('desde', blank=True)
	hora_hasta = models.TimeField('hasta', blank=True)
	dia_semana = models.IntegerField(default=0, blank=True)
	

class Espacio(models.Model):
	pass
	
