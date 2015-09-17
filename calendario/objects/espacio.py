# -*- coding: utf-8 -*-
import time
from random import random, randrange

from django.db import models

from especialidad import Especialidad
from profesional import Profesional

PUNTOS_RESTRICCION_PROFESIONAL = 3
PUNTOS_HORAS_SEMANALES = 2
PUNTOS_HORAS_DIARIAS = 1
PUNTOS_DISTRIBUCION_HORARIA = 1

class Espacio(models.Model):
	"""
	Clase que abarca el medio ambiente
	en el cual se desarrolla el algoritmo.
	
	@Atributos:
	.dias_habiles - lista con los dias a cubrir. Valor: {}.
	.horarios - diccionario con los horarios a cubrir. Valor: {}.
	.poblacion - lista de individuos. Valor: [].
	.generaciones - cantidad de generaciones a generar. Valor: 0.
	"""
	
	nombre = models.CharField(max_length=100, null=False, blank=False)
	estado = models.CharField(max_length=3,
								choices=[('ON', 'ON'), ('OFF', 'OFF')],
								default='ON')
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
		espacio._generaciones = generaciones
		
		#HARDCODED
		espacio._dias_habiles = [1, 2, 3, 4, 5]
		
		return espacio
	
	def __str__(self, ):
		return unicode(self.nombre)
	
	def setnombre(self, nombre):
		
		if nombre == "":
			raise Exception("El nombre no puede estar vacío.")
		
		self.nombre = nombre
	
	# GENETIC ALGORITHMS
	
	def generarpoblacioninicial(self, ):
		"""
		Genera individuos desde cero y
		los guarda en el atributo 'poblacion'.
		
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
			
			#Cantidad de iteraciones por los horarios.
			for hora in self.horas:
				
				#Iteracion por cada coordinador.
				for coordinador in self.coordinadores:
					
					#Se crea un Calendario.
					calendario = Calendario.create()
					#Se le asigna este espacio.
					calendario.espacio = self
					#A su vez el Calendario es agregado a la poblacion.
					self.poblacion.append(calendario)
					
					#Se crea un Horario.
					horario = Horario()
					#Se le asigna una Especialidad.
					horario.especialidad = coordinador.especialidad
					#Se le asigna una Profesional.
					horario.profesional = coordinador.profesional
					#Se le asigna una hora desde.
					horario.hora_desde = hora.hora_desde
					#Se le asigna una hora hasta.
					horario.hora_hasta = hora.hora_hasta
					#Se le asigna un dia de la semana.
					horario.dia_semana = dia
					#El Horario es agregado al Calendario.
					calendario.agregar_horario(horario)
					
		
		#Rellenamos el Calendario generando Horarios aleatorios.
		
		#Por cada Calendario en la poblacion.
		for calendario in self.poblacion:
			
			#Iteramos por la cantidad de dias.
			for dia in range(0, 7):
				
				if dia not in self.dias_habiles:
					continue
				
				#Tambien por la cantidad de horarios.
				for hora in self.horas:
					
					#Obtenemos un indice aleatorio.
					indice = randrange(0, len(self.coordinadores))
					
					#Obtenemos un coordinador aleatoriamente.
					coordinador = self.coordinadores[indice]
					
					#Se crea un Horario.
					horario = Horario()
					#Se le asigna una Especialidad.
					horario.especialidad = coordinador.especialidad
					#Se le asigna una Profesional.
					horario.profesional = coordinador.profesional
					#Se le asigna una hora desde.
					horario.hora_desde = hora.hora_desde
					#Se le asigna una hora hasta.
					horario.hora_hasta = hora.hora_hasta
					#Se le asigna un dia de la semana.
					horario.dia_semana = dia
					
					#Comprobamos que el Horario generado
					#no exista en el Calendario.
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
		
	
	def ejecutar(self, ):
		
		global_time = time.time()
		
		operation_time = time.time()
		
		self.generarpoblacioninicial()
		
		print "Población inicial generada en %7.3f seg." % (time.time() - operation_time)
		
		#Descomentar para evaluaciones
		#~ self.poblacion = self.poblacion[:1]
		
		operation_time = time.time()
		
		self.fitness()
		
		print "Evaluación realizada en %7.3f seg." % (time.time() - operation_time)
		
		operation_time = time.time()
		
		#Ordenamos la lista ubicando los individuos más aptos de principio a fin.
		#~ self.poblacion.sort()
		
		print "El ordenamiento de %d calendarios tardó %7.3f seg." % (len(self.poblacion), time.time() - operation_time)
		
		#Cortamos la lista, quedándonos con los 100 individuos más aptos.
		self.poblacion = self.poblacion[:100]
		
		operation_time = time.time()
		
		for calendario in self.poblacion:
			calendario.full_save()
		
		print "Guardar %d calendarios llevó %7.3f seg." % (len(self.poblacion), time.time() - operation_time)
		
		print
		print "La evolución tardó %7.3f seg." % (time.time() - global_time)
	
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
		
		#Por cada individuo en la poblacion.
		for calendario in self.poblacion:
			
			#Si el individuo ya fue evaluado seguimos con otro.
			if calendario.puntaje != 0:
				continue
			
			#Primera evaluacion: Se evalua que los horarios asignados
			#cumplan las restricciones del profesional que contienen.
			
			#Comparamos los horarios con las restricciones de los
			#profesionales. Cada superposicion es penalizada,
			#mientras mas alto sea el puntaje, menos apto es el individuo.
			
			#Por cada franja de horarios.
			#~ for franja_horaria in calendario.horarios:
				
				#~ #Por cada horario dentro de la franja.
				#~ for horario in franja_horaria:
					
					#~ #Por cada restriccion del profesional.
					#~ for restriccion in horario.profesional.restricciones.all():
						
						#~ #Si no es el mismo dia de la semana del horario continuamos.
						#~ if restriccion.dia_semana != 7 and horario.dia_semana != restriccion.dia_semana:
							#~ continue
						
						#~ if (horario.hora_desde >= restriccion.hora_desde and horario.hora_desde < restriccion.hora_hasta):
							#~ calendario.puntaje += PUNTOS_RESTRICCION_PROFESIONAL
							#~ break
						#~ if (horario.hora_hasta > restriccion.hora_desde and horario.hora_hasta <= restriccion.hora_hasta):
							#~ calendario.puntaje += PUNTOS_RESTRICCION_PROFESIONAL
							#~ break
						#~ if (horario.hora_desde <= restriccion.hora_desde and horario.hora_hasta >= restriccion.hora_hasta):
							#~ calendario.puntaje += PUNTOS_RESTRICCION_PROFESIONAL
							#~ break
						#~ if (horario.hora_desde > restriccion.hora_desde and horario.hora_hasta < restriccion.hora_hasta):
							#~ calendario.puntaje += PUNTOS_RESTRICCION_PROFESIONAL
							#~ break
						#~ if (horario.hora_desde == restriccion.hora_desde and horario.hora_hasta == restriccion.hora_hasta):
							#~ calendario.puntaje += PUNTOS_RESTRICCION_PROFESIONAL
			
			
			#~ #Segunda evaluacion: Que se cumplan las horas semanales de la especialidad.
			#~ #Horas semanales: cada hora extra o faltante es penalizada con la suma de puntos.
			
			#~ #Por cada especialidad
			#~ for especialidad in self.especialidades.all():
				
				#~ #Contador de horas semanales.
				#~ horas_semanales = 0
				#~ #Por cada franja de horarios.
				#~ for franja_horaria in calendario.horarios:
					
					#~ #Por cada horario en la franja horaria.
					#~ for horario in franja_horaria:
						
						#~ #Si la especialidad es igual, contamos.
						#~ if horario.especialidad == especialidad:
							#~ horas_semanales += 1
					
				#~ calendario.puntaje += abs(especialidad.carga_horaria_semanal - horas_semanales) * PUNTOS_HORAS_SEMANALES
			
			#~ #Tercera evaluacion: Se busca que las especialidades
			#~ #cumplan con la horas maximas por dia.
			#~ #Horas maxima por dia: Cada especialidad tiene un
			#~ #atributo max_horas_diaria, en el caso que un calendario
			#~ #exceda este valor recibira una penalizacion.
			
			#~ for i in range(len(self.dias_habiles)):
				
				#~ for j in range(len(self.horas)):
					
					#~ horas_diarias = 1
					
					#~ #Obtenemos el horario a evaluar.
					#~ horario = calendario.horarios[j][i]
					
					#~ for k in range(len(self.dias_habiles)):
						
						#~ #Si el dia no es el mismo, lo salteamos.
						#~ if i != k:
							#~ continue
						
						#~ for l in range(len(self.horas)):
							
							#~ if j >= l:
								#~ continue
							
							#~ #Obtenemos el horario a comparar.
							#~ horario_comp = calendario.horarios[l][k]
							
							#~ #Si la especialidad es la misma, contamos.
							#~ if horario.especialidad == horario_comp.especialidad:
								#~ horas_diarias += 1
						
						#~ #Si la cantidad máxima de horas diarias
						#~ #se excedieron, penalizamos.
						#~ if horas_diarias > horario.especialidad.max_horas_diaria:
							#~ calendario.puntaje += (horas_diarias - horario.especialidad.max_horas_diaria) * PUNTOS_HORAS_DIARIAS
						
						#~ break
					
			
			#Cuarta evaluación: En esta instancia se desea comprobar
			#la distribución horaria de las especialidades.
			#Horas semanales: cada hora extra o faltante es
			#penalizada con la suma de puntos.
			
			for i in range(len(self.dias_habiles)):
				
				for j in range(len(self.horas)):
					
					horas_diarias = 1
					
					#Obtenemos el horario a evaluar.
					horario = calendario.horarios[j][i]
					
					for k in range(len(self.dias_habiles)):
						
						#Si el dia no es el mismo, lo salteamos.
						if i != k:
							continue
						
						for l in range(len(self.horas)):
							
							if j >= l:
								continue
							
							#Obtenemos el horario a comparar.
							horario_comp = calendario.horarios[l][k]
							
							#Si las especialidades son distintas no
							#tenemos que evaluarlo, por ende lo salteamos.
							if horario.especialidad != horario_comp.especialidad:
								continue
							
							if j + 1 == l:
								continue
							
							#Esta comprobación se hace para que no se
							#penalice M M M.
							#~ penalizable = False
							#~ m = l - 1
							#~ while j != m:
								
								#~ if horario.especialidad != calendario.horarios[m][k].especialidad:
									#~ penalizable = True
									#~ break
								
								#~ m -= 1
							
							#~ if not penalizable:
								#~ continue
							
							#~ if self.poblacion[0] == calendario:
								#~ print horario.especialidad
								#~ print "%d - %d" % (j, l)
								#~ print horario.dia_semana
							
							calendario.puntaje += PUNTOS_DISTRIBUCION_HORARIA
							
							#La asignación se realiza si queremos que
							#no se penalice esto M L L M M.
							#~ horario = horario_comparacion
							
			
	
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
	def horas(self, ):
		from hora import Hora
		
		if not self._horas:
			self._horas = Hora.objects.filter(espacio=self)\
										.order_by('hora_desde')
		
		return self._horas
	
	@property
	def coordinadores(self, ):
		from coordinador import Coordinador
		
		if not self._coordinadores:
			self._coordinadores = Coordinador.objects.filter(espacio=self)\
														.order_by('especialidad')
		
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
	
