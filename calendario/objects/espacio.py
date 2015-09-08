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
	def create(cls, espacio_id=0, generaciones=0):
		
		espacio = None
		
		if espacio_id != 0:
			espacio = Espacio.objects.get(pk=espacio_id)
		else:
			espacio = Espacio()
		
		espacio._calendarios = []
		espacio._horas = []
		espacio._coordinadores = []
		espacio._poblacion = []
		espacio._restricciones = []
		espacio._generaciones = generaciones
		
		#HARDCODED
		espacio._dias_habiles = [1, 2, 3, 4, 5]
		
		return espacio
	
	def __str__(self, ):
		return unicode(self.nombre)
	
	@property
	def horas(self, ):
		from hora import Hora
		
		if not self._horas:
			self._horas = Hora.objects.filter(espacio=self).order_by('hora_desde')
		
		return self._horas
	
	@property
	def coordinadores(self, ):
		from coordinador import Coordinador
		
		if not self._coordinadores:
			self._coordinadores = Coordinador.objects.filter(espacio=self).order_by('hora_desde')
		
		return self._coordinadores
	
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
	
	def generarpoblacioninicial(self, ):
		"""
		Genera individuos desde cero y los guarda en el atributo 'poblacion'.
		
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
					
					for profesional in self.profesionales.all():
						for pespecialidad in profesional.especialidades.all():
							if especialidad.nombre == pespecialidad.nombre:
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
					horario.especialidad = self.especialidades.all()[randrange(0, len(self.especialidades.all()))] #Se le asigna una Especialidad.
					
					for profesional in self.profesionales.all():
						for pespecialidad in profesional.especialidades.all():
							if especialidad.nombre == pespecialidad.nombre:
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
		
	
	def evolucionar(self, ):
		print "FITNESS"
		self.fitness()
		
		#Ordenamos la lista ubicando los individuos más aptos de principio a fin.
		self.poblacion.sort()
		
		#Cortamos la lista, quedándonos con los 100 individuos más aptos.
		self.poblacion = self.poblacion[:100]
		
		for calendario in self.poblacion:
			calendario.full_save()
	
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
			#los profesionales. Cada superposicion es penalizada, mientras mas
			#alto sea el puntaje, menos apto es el individuo.
			
			for franja_horaria in calendario.horarios: #Por cada franja de horarios.
				
				for horario in franja_horaria: #Por cada horario dentro de la franja.
					
					for restriccion in horario.profesional.restricciones.all(): #Por cada restriccion del profesional.
						
						if horario.dia_semana != restriccion.dia_semana: #Si no es el mismo dia de la semana del horario continuamos.
							continue
						
						if (horario.hora_desde >= restriccion.hora_desde and horario.hora_desde < restriccion.hora_hasta) or \
							(horario.hora_hasta > restriccion.hora_desde and horario.hora_hasta <= restriccion.hora_hasta) or \
							(horario.hora_desde <= restriccion.hora_desde and horario.hora_hasta >= restriccion.hora_hasta):
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
					
				#Esta linea se puede comentar?
				if horas_semanales != especialidad.carga_horaria_semanal:
					calendario.puntaje += abs(especialidad.carga_horaria_semanal - horas_semanales) * self.PUNTOS_HORAS_SEMANALES
			
			#Tercera evaluacion: Se busca que las especialidades cumplan con la horas maximas por dia.
			#Horas maxima por dia: Cada especialidad tiene un atributo max_horas_diaria,
			#en el caso que un calendario exceda este valor recibira una penalizacion.
			
			#DECIDIR LA MANERA EN LA QUE SE RECORRE ESTE TIPO DE PENALIZACION.
			#POR ESPECIALIDAD O POR HORARIO, PROGRAMATICAMENTE POR ESPECIALIDAD ES MAS SENCILLA.
			
			for franja_horaria in calendario.horarios: #Por cada franja de horarios.
				
				for horario in franja_horaria: #Por cada horario dentro de la franja.
					
					horas_diarias = 1
					
					for franja_horaria_comparacion in calendario.horarios: #Por cada franja de horarios.
						
						for horario_comparacion in franja_horaria: #Por cada horario dentro de la franja.
							
							if horario == horario_comparacion:
								break
							
							if horario.especialidad == horario_comparacion.especialidad:
								horas_diarias += 1
					
					if horas_diarias != horario.especialidad.max_horas_diaria:
						calendario.puntaje += abs(especialidad.max_horas_diaria - horas_diarias) * self.PUNTOS_HORAS_DIARIAS
					
			
			#Cuarta evaluacion: En esta instancia se desea comprobar la distribución horaria de las especialidades.
			#Horas semanales: cada hora extra o faltante es penalizada con la suma de puntos.
			
			for franja_horaria in calendario.horarios: #Por cada franja de horarios.
				
				for horario in franja_horaria: #Por cada horario dentro de la franja.
					
					for franja_horaria_comparacion in calendario.horarios: #Por cada franja de horarios.
						
						for horario_comparacion in franja_horaria_comparacion: #Por cada horario dentro de la franja.
							
							if horario == horario_comparacion:
								break
							
							if horario.especialidad != horario_comparacion.especialidad:
								break
							
							#~ if horario not in franja_horaria:
								#~ print str(horario) + " no está en " + str(franja_horaria)
								#~ continue
							
							#~ if horario_comparacion not in franja_horaria_comparacion:
								#~ print str(horario_comparacion) + " no está en " + str(franja_horaria_comparacion)
								#~ continue
							
							#Una mejor manera de obtener el index.
							
							if calendario.horarios.index(franja_horaria) + 1 == calendario.horarios.index(franja_horaria_comparacion):
								horario = horario_comparacion
							else:
								calendario.puntaje += self.PUNTOS_DISTRIBUCION_HORARIA
			
			#~ calendario.save()
			
	
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
	
