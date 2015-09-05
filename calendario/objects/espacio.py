# -*- coding: utf-8 -*-
from random import random, randrange
from django.db import models
from especialidad import Especialidad
from profesional import Profesional

class Espacio(models.Model):
	"""
	Clase que abarca el medio ambiente en el cual se desarrolla el algoritmo.
	
	@Atributos:
	.dias_habiles - lista con los dias a cubrir. Valor: {}.
	.horarios - diccionario con los horarios a cubrir. Valor: {}.
	.poblacion - lista de individuos. Valor: [].
	.generaciones - cantidad de generacion a generar. Valor: 0.
	"""
	
	PUNTOS_RESTRICCION_PROFESIONAL = 3
	PUNTOS_HORAS_SEMANALES = 2
	PUNTOS_HORAS_DIARIAS = 1
	PUNTOS_DISTRIBUCION_HORARIA = 1
	
	nombre = models.CharField(max_length=100, null=False, blank=False)
	estado = models.CharField(max_length=3, choices=[('ON', 'ON'), ('OFF', 'OFF')], default='ON')
	usuario_creador = models.CharField(max_length=30, default='admin')
	fecha_creacion = models.DateField(auto_now_add=True)
	usuario_modificador = models.CharField(max_length=30, default='admin')
	fecha_modificacion = models.DateField(auto_now=True)
	
	especialidades = models.ManyToManyField(Especialidad)
	profesionales = models.ManyToManyField(Profesional)
	
	@classmethod
	def create(cls, espacio_id=0):
		
		espacio = None
		
		if espacio_id != 0:
			espacio = Espacio.objects.get(pk=espacio_id)
		else:
			espacio = Espacio()
		
		espacio._calendarios = []
		espacio._horas = []
		espacio._poblacion = []
		espacio._restricciones = []
		espacio._generaciones = 0
		
		#HARDCODED
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
	def calendarios(self, ):
		from calendario import Calendario
		
		if not self._calendarios:
			self._calendarios = Calendario.objects.filter(espacio=self)
		
		return self._calendarios
	
	def setnombre(self, nombre):
		
		if nombre == "":
			raise Exception("El nombre no puede estar vacío.")
		
		self.nombre = nombre
	
	# GENETIC ALGORITHMS
	
	def generar_poblacion_inicial(self, ):
		"""
		Crea la poblacion inicial de individuos y los guarda en el atributo 'poblacion'.
		
		@Parametros:
		None
		
		@Return:
		None
		"""
		from calendario import Calendario
		from horario import Horario
		#Iteramos generando todas las combinaciones posibles de horarios.
		#Y agregamos cada uno a un calendario.
		for dia in range(0, 7): #Cantidad de iteraciones por los dias.
			
			if dia not in self.dias_habiles:
				continue
			
			for hora in self.horas: #Cantidad de iteraciones por los horarios.
				
				for especialidad in self.especialidades.all(): #Iteracion por cada especialidad.
					
					calendario = Calendario.create() #Se crea un Calendario.
					
					calendario.espacio = self #Se le asigna este espacio.
					
					self.poblacion.append(calendario) #A su vez el Calendario es agregado a la poblacion.
					
					horario = Horario() #Se crea un Horario.
					horario.especialidad = especialidad #Se le asigna una Especialidad.
					horario.profesional = profesional #Se le asigna un Profesional.
					horario.hora_desde = hora.hora_desde #Se le asigna una hora desde.
					horario.hora_hasta = hora.hora_hasta #Se le asigna una hora hasta.
					horario.dia_semana = dia #Se le asigna un dia de la semana.
					
					calendario.agregar_horario(horario) #El Horario es agregado al Calendario.
					
		
		#Rellenamos el Calendario generando Horarios aleatorios.
		for calendario in self.poblacion: #Por cada Calendario en la poblacion.
			
			for dia in range(0, 7): #Iteramos por la cantidad de dias.
				
				if dia not in self.dias_habiles:
					continue
				
				for hora in self.horas: #Tambien por la cantidad de horarios.
					
					horario = Horario() #Se crea un Horario.
					horario.especialidad = self.especialidades.all()[randrange(0, len(self.especialidades.all()))] #Se le asigna un Especialidad.
					horario.profesional = profesional #Se le asigna un Profesional.
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
		
		#~ for calendario in self.poblacion:
			#~ calendario.full_save()
	
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
			
			
			for franja_horaria in calendario.horarios: #Por cada franja de horarios.
				
				for horario in franja_horaria: #Por cada por cada horario dentro de la franja.
					
					for restriccion in horario.especialidad.profesional.restricciones.all(): #Por cada restriccion del profesional.
						
						if horario.dia_semana != restriccion.dia_semana: #Si no es el mismo dia de la semana del horario continuamos.
							continue
						
						if (horario.desde >= restriccion.desde and horario.desde < restriccion.hasta) or \
							(horario.hasta > restriccion.desde and horario.hasta <= restriccion.hasta) or \
							(horario.desde <= restriccion.desde and horario.hasta >= restriccion.hasta):
							calendario.puntaje += self.PUNTOS_RESTRICCION_PROFESIONAL
			
			
			#Segunda evaluacion: Que se cumplan las horas semanales y diarias de la especialidad.
			#Horas semanales: cada hora extra o faltante es penalizada con la suma de puntos.
			
			for especialidad in self.especialidades.all(): #Por cada especialidad
				
				horas_semanales = 0 #Contador de horas semanales.
				for franja_horaria in calendario.horarios: #Por cada franja de horarios.
					
					for horario in franja_horaria: #Por cada horario en la franja horaria.
						
						#Si la especialidad es igual, contamos.
						if horario.especialidad == especialidad:
							horas_semanales += 1
					
				if horas_semanales != especialidad.carga_horaria_semanal:
					calendario.puntaje += abs(especialidad.carga_horaria_semanal - horas_semanales) * self.PUNTOS_HORAS_SEMANALES
			
			#~ for i in range(len(self.dias_habiles)):
				#~ 
				#~ for j in self.horas:
					#~ pass
			
			calendario.save()	
			
	
	def seleccionar(self, ):
		pass
	
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
	
