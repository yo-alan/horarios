# -*- coding: utf-8 -*-
from random import random, randrange
from django.db import models
from objects.espacio import Espacio
from objects.hora import Hora
from objects.persona import Persona
from objects.profesional import Profesional
from objects.especialidad import Especialidad
from objects.calendario import Calendario
from objects.horario import Horario
from objects.restriccion import Restriccion
from objects.espacio_restriccion import Espacio_restriccion
from objects.profesional_restriccion import Profesional_restriccion


class Entorno(object):
	"""
	Clase que abarca el medio ambiente en el cual se desarrolla el algoritmo.
	
	@Atributos:
	.dias_habiles - lista con los dias a cubrir. Valor: {}.
	.horarios - diccionario con los horarios a cubrir. Valor: {}.
	.poblacion - lista de individuos. Valor: [].
	.generaciones - cantidad de generacion a generar. Valor: 0.
	.espacio - espacio para el cual se generan los individuos. Valor: None.
	"""
	
	PUNTOS_RESTRICCION_PROFESIONAL = 3
	PUNTOS_HORAS_SEMANALES = 2
	PUNTOS_HORAS_DIARIAS = 1
	PUNTOS_DISTRIBUCION_HORARIA = 1
	
	_poblacion = []
	_generaciones = 0
	_espacio = None
	
	def __init__(self, generaciones=50, espacio=None):
		"""
		Inicializa los atributos del objeto.
		
		@Parametros:
		generaciones - cantidad de generaciones a generar. Valor: 50.
		espacio - El espacio para el cual se generaran los calendarios. Valor: None.
		
		@Return:
		None
		"""
		
		self.generaciones = generaciones
		self.espacio = espacio
	
	def generar_poblacion_inicial(self, ):
		"""
		Crea la poblacion inicial de individuos y los guarda en el atributo 'poblacion'.
		
		@Parametros:
		None
		
		@Return:
		None
		"""
		
		#Iteramos generando todas las combinaciones posibles de horarios.
		#Y los agregamos a un calendario.
		for dia in range(0, 7): #Cantidad de iteraciones por los dias.
			
			if dia not in self.espacio.dias_habiles:
				continue
			
			for hora in self.espacio.horas: #Cantidad de iteraciones por los horarios.
				
				for especialidad in self.espacio.especialidades: #Iteracion por cada especialidad.
					
					calendario = Calendario.create() #Se crea un Calendario.
					calendario.limpiar()
					calendario.espacio = self.espacio #Se le asigna el espacio.
					#~ calendario.save() #Y se guarda.
					
					self.poblacion.append(calendario) #A su vez el Calendario es agregado a la poblacion del Entorno.
					
					horario = Horario() #Se crea un Horario.
					horario.especialidad = especialidad #Se le asigna un Especialidad.
					horario.hora_desde = hora.hora_desde #Se le asigna una hora desde.
					horario.hora_hasta = hora.hora_hasta #Se le asigna una hora hasta.
					horario.dia_semana = dia #Se le asigna un dia de la semana.
					
					calendario.agregar_horario(horario) #El Horario es agregado a la lista del Calendario.
					
		
		#Rellenamos el Calendario generando Horarios aleatorios.
		for calendario in self.poblacion: #Por cada Calendario en la poblacion.
			
			for dia in range(0, 7): #Iteramos por la cantidad de dias.
				
				if dia not in self.espacio._dias_habiles:
					continue
				
				for hora in self.espacio.horas: #Tambien por la cantidad de horarios.
					
					horario = Horario() #Se crea un Horario.
					horario.especialidad = self.espacio.especialidades[randrange(1, len(self.espacio.especialidades))] #Se le asigna un Especialidad.
					horario.hora_desde = hora.hora_desde #Se le asigna una hora desde.
					horario.hora_hasta = hora.hora_hasta #Se le asigna una hora hasta.
					horario.dia_semana = dia #Se le asigna un dia de la semana.
					#~ horario.calendario = calendario #Se le asigna el calendario.
					
					#Comprobamos que el Horario generado no exista en el Calendario.
					existe = False
					for franja_horaria in calendario.horarios:
						for horario_comp in franja_horaria:
							if horario == horario_comp:
								existe = True
					
					#Si ya existe continuamos generando.
					if existe:
						continue
					
					#Y lo agregamos a la lista de horarios del Calendario
					calendario.agregar_horario(horario)
		
		for calendario in self.poblacion:
			calendario.full_save()
	
	def evolucionar(self, ):
		print "FITNESS"
		self.fitness()
	
	def fitness(self, ):
		"""
		Asigna un puntaje a los calendarios.
		Utiliza las restricciones de los profesionales para
		determinar el valor de aptitud de los individuos.
		
		@Parametros:
		None
		
		@Return:
		None
		"""
		
		#Primera evaluacion: Que los horarios asignados cumplan las restricciones.
		
		for calendario in self.poblacion: #Por cada individuo en la poblacion.
			
			#Si el individuo ya fue evaluado seguimos con otro.
			if calendario.puntaje != 0:
				continue
			
			#Comparamos los horarios con las restricciones de
			#los profesionales. Cada superposicion vale un punto, mientras mas
			#alto sea el puntaje, menos apto es el individuo.
			
			for restriccion in self.restricciones: #Por cada restriccion.
				
				for franja_horaria in calendario.horarios: #Por cada franja de horarios.
					
					for horario in franja_horaria: #Por cada por cada horario dentro de la franja.
						
						for especialidad in self.espacio.especialidades: #Por cada especialidad.
							
							if horario.especialidad.profesional != especialidad.profesional: #Si no es el profesional del horario continuamos.
								continue
							
							if horario.dia_semana != restriccion.dia_semana: #Si no es el mismo dia de la semana del horario continuamos.
								continue
							
							if (horario.desde >= restriccion.desde and horario.desde < restriccion.hasta) or \
								(horario.hasta > restriccion.desde and horario.hasta <= restriccion.hasta) or \
								(horario.desde <= restriccion.desde and horario.hasta >= restriccion.hasta):
								calendario.puntaje += PUNTOS_RESTRICCION_PROFESIONAL
			
			
			#Segunda evaluacion: Que se cumplan las horas semanales y diarias de la especialidad.
			#Horas semanales: cada hora extra o faltante es penalizada con la suma de puntos.
			
			for especialidad in self.espacio.especialidades: #Por cada especialidad
				
				horas_semanales = 0 #Contador de horas semanales.
				for franja_horaria in calendario.horarios: #Por cada franja de horarios.
					
					for horario in franja_horaria: #Por cada horario en la franja horaria.
						
						#Si la especialidad es igual, contamos.
						if horario.profesional.especialidad == especialidad:
							horas_semanales += 1
					
				if horas_semanales != especialidad.carga_horaria_semanal:
					#~ calendario.puntaje += abs(especialidad.carga_horaria_semanal - horas_semanales)
					calendario.puntaje += PUNTOS_HORAS_SEMANALES
			
			for i in range(len(self.espacio._dias_habiles)):
				
				for j in self.espacio.horas:
					pass
				
			
	
	def seleccionar(self, ):
		pass
	
	@property
	def espacio(self, ):
		return self._espacio
	
	@espacio.setter
	def espacio(self, espacio):
		self._espacio = espacio
	
	@property
	def generaciones(self, ):
		return self._generaciones
	
	@generaciones.setter
	def generaciones(self, generaciones):
		self._generaciones = generaciones
	
	@property
	def poblacion(self, ):
		return self._poblacion
	
	@poblacion.setter
	def poblacion(self, poblacion):
		self._poblacion = poblacion
	
	@property
	def restricciones(self, ):
		return self._restricciones
	
	@restricciones.setter
	def restricciones(self, restricciones):
		self._restricciones = restricciones
	
	@property
	def dias(self, ):
		return self._dias
	
	@dias.setter
	def dias(self, dias):
		self._dias = dias
	
