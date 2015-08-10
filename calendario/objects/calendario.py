# -*- coding: utf-8 -*-
from django.db import models
from espacio import Espacio

class Calendario(models.Model):
	
	espacio = models.ForeignKey(Espacio)
	puntaje = models.IntegerField(default=0)
	
	@classmethod
	def create(cls, calendario_id=0):
		
		calendario = None
		
		if calendario_id != 0:
			calendario = Calendario.objects.get(pk=calendario_id)
		else:
			calendario = Calendario()
		
		calendario._horarios = []
		
		return calendario
	
	def __str__(self, ):
		return str(self.espacio) + "(" + str(self.id) + ")"
	
	#Por cada franja horaria de uso se inserta una nueva lista de horarios vacia
	######################################################
	#~ for dia in dias:
		#~ horarios.append([])
	######################################################
	
	def cruce(self, madre, prob_mutacion=0.01):
		"""
		Cruza el individuo con otro madre.
		
		@Parametros:
		madre - individuo con quien realizar la cruza.
		prob_mutacion - probabilidad de mutacion para los hijos resultantes. Valor: 0.01.
		
		@Return:
		
		"""
		if not isinstance(madre, Calendario):
			raise Exception("El objeto no es de tipo Calendario.")
		
		if self == madre:
			raise Exception("Un Calendario no puede cruzarse consigo mismo.")
		
		
		
	
	def mutar(self, ):
		pass
	
	def limpiar(self, ):
		self._horarios = []
	
	def agregar_horario(self, horario):
		"""
		Agrega un Horario a la lista de horarios del Calendario.
		"""
		
		for franja_horaria in self._horarios: #Por cada dia.
			#Si contiene un Horario con mismo dia_desde lo agrega a la lista
			if franja_horaria[0].hora_desde == horario.hora_desde:
				franja_horaria.append(horario)
				return
		
		#Sino crea una nueva lista con el Horario
		self._horarios.append([horario])
	
	def full_save(self, ):
		
		#Se guarda el mismo para obtener una ID de la BBDD.
		self.save()
		
		for franja_horaria in self.horarios: #Por cada dia.
			#Guarda todos y cada uno de los horarios que posee.
			for horario in franja_horaria:
				horario.calendario = self
				horario.save()
	
	@property
	def horarios(self, ):
		
		if not self._horarios:
			horarios = Horario.objects.filter(calendario=self).order_by('hora_desde', 'dia_semana')
			
			for horario in horarios:
				self.agregar_horario(horario)
		
		return self._horarios
	
