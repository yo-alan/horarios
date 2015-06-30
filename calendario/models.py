from random import random, randrange
from django.db import models


class Especialidad(models.Model):
	
	nombre = models.CharField(max_length=100, null=False)
	carga_horaria_semanal = models.IntegerField(default=0, null=False)
	max_horas_diaria = models.IntegerField(default=0, null=False)
	
	def __str__(self, ):
		return self.nombre.encode('utf-8')
	
	def __eq__(self, o):
		return self.nombre == o.nombre
	

class Espacio(models.Model):
	
	nombre = models.CharField(max_length=100, null=False, blank=False)
	
	def __str__(self, ):
		return self.nombre

class Persona(models.Model):
	
	nombre = models.CharField(max_length=100, null=False, blank=False)
	apellido = models.CharField(max_length=100, null=False, blank=False)
	cuil = models.CharField(max_length=11, unique=True, null=False, blank=False)

class Profesional(Persona):
	
	restricciones = []
	especialidad = models.ForeignKey(Especialidad)
	
	def __str__(self, ):
		return self.apellido.encode('utf-8') + ", " + self.nombre.encode('utf-8')
	
	def __eq__(self, o):
		return self.cuil == o.cuil

class Calendario(models.Model):
	
	espacio = models.ForeignKey(Espacio)
	horarios = []
	puntaje = models.IntegerField(default=0)
	
	def getHorarios(self, ):
		"""
		Actualiza los horarios del Calendario.
		
		@Parametros:
		None
		
		@Return:
		lista de horarios.
		"""
		
		#Trae los horarios del Calendario de la BBDD.
		hs = Horario.objects.filter(calendario=self).order_by('hora_desde', 'dia_semana')
		
		self.horarios = [] #Setea a vacia su lista actual.
		
		#Y agrega los que recibio de la BBDD.
		for h in hs:
			self.agregar_horario(h)
		
		return self.horarios
	
	def agregar_horario(self, horario):
		"""
		Agrega un Horario a la lista de horarios del Calendario.
		"""
		
		for dia in self.horarios: #Por cada dia.
			#Si contiene un Horario con mismo dia_desde lo agrega a la lista
			if dia[0].hora_desde == horario.hora_desde:
				dia.append(horario)
				return
		
		#Sino crea una nueva lista con el Horario
		self.horarios.append([horario])
	
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
	

class Horario(models.Model):
	
	hora_desde = models.TimeField('desde', null=False)
	hora_hasta = models.TimeField('hasta', null=False)
	dia_semana = models.IntegerField(default=0, null=False)
	calendario = models.ForeignKey(Calendario)
	profesional = models.ForeignKey(Profesional)
	
	def __str__(self, ):
		#~ return str(self.profesional.especialidad)
		return str(self.hora_desde)
	
	def __eq__(self, o):
		return self.hora_desde == o.hora_desde and self.hora_hasta == o.hora_hasta and self.dia_semana == o.dia_semana and self.calendario == o.calendario
	

class Restriccion(models.Model):
	
	hora_desde = models.TimeField('desde', null=False, blank=False)
	hora_hasta = models.TimeField('hasta', null=False, blank=False)
	dia_semana = models.IntegerField(default=0, null=False, blank=False)
	
	def __eq__(self, o):
		pass
		#return self.hora_desde == o.hora_desde and self.hora_hasta == o.hora_hasta and self.

class Espacio_restriccion(Restriccion):
	
	espacio = models.ForeignKey(Espacio)

class Profesional_restriccion(Restriccion):
	
	profesional = models.ForeignKey(Profesional)

class Entorno(object):
	"""
	Clase que abarca el medio ambiente en el cual se desarrolla el algoritmo.
	
	@Atributos:
	.DIAS - constante con los dias de la semana. Valor: {}.
	.dias_habiles - lista con los dias a cubrir. Valor: {}.
	.horarios - diccionario con los horarios a cubrir. Valor: {}.
	.poblacion - lista de individuos. Valor: [].
	.restricciones - lista de restricciones. Valor: [].
	.generaciones - cantidad de generacion a generar. Valor: 0.
	.espacio - espacio para el cual se generan los individuos. Valor: None.
	"""
	
	DIAS = {0 : "Domingo", 1 : "Lunes", 2 : "Martes", 3 : "Miercoles", 4 : "Jueves", 5 : "Viernes", 6 : "Sabado"}
	
	#HARDCODED
	_dias_habiles = [1, 2, 3, 4, 5]
	_horarios = {1 : "7:30", 2 : "8:10", 3 : "9:00", 4 : "9:40", 5 : "10:30", 6 : "11:10", 7 : "11:50"}
	
	_poblacion = []
	_restricciones = []
	_generaciones = 0
	_espacio = None
	
	def __init__(self, generaciones=50, espacio=None):
		"""
		Inicializa los atributos del objeto.
		
		@Parametros:
		generaciones - cantidad de generaciones a generar. Valor: 50.
		espacio - . Valor: None.
		
		@Return:
		None
		"""
		
		self.restricciones = Restriccion.objects.all() #Asignamos todas las restricciones de la BBDD.
		self.generaciones = generaciones
		self.espacio = espacio
		
		self.generar_poblacion_inicial()
	
	def generar_poblacion_inicial(self, ):
		"""
		Crea la poblacion inicial de individuos y los guarda en el atributo 'poblacion'.
		
		@Parametros:
		None
		
		@Return:
		None
		"""
		
		#Obtenemos los profesionales de la BBDD.
		ps = Profesional.objects.all()
		
		#Iteramos generando todas las combinaciones posibles de horarios.
		#Y los agregamos a un calendario.
		for dia in range(0, 7): #Cantidad de iteraciones por los dias.
			
			if dia not in self.dias_habiles:
				continue
			
			for horario in range(1, len(self.horarios)): #Cantidad de iteraciones por los horarios.
				for p in ps: #Iteracion por cada profesional.
					
					c = Calendario() #Se crea un Calendario.
					c.espacio = self.espacio #Se le asigna el espacio.
					c.save() #Y se guarda.
					
					h = Horario() #Se crea un Horario.
					h.profesional = p #Se le asigna un Profesional.
					h.hora_desde = self.horarios[horario] #Se le asigna una hora desde.
					h.hora_hasta = self.horarios[horario+1] #Se le asigna una hora hasta.
					h.dia_semana = dia #Se le asigna un dia de la semana.
					h.calendario = c #Se le asigna el calendario.
					h.save() #Y se guarda.
					
					c.agregar_horario(h) #El Horario es agregado a la lista del Calendario.
					
					self.poblacion.append(c) #A su vez el Calendario es agregado a la poblacion del Entorno.
					
		
		#Rellenamos el Calendario generando Horarios aleatorios.
		for c in self.poblacion: #Por cada Calendario en la poblacion.
			
			for dia in range(0, 7): #Iteramos por la cantidad de dias.
				
				if dia not in self.dias_habiles:
					continue
				
				for horario in range(1, len(self.horarios)): #Tambien por la cantidad de horarios.
					
					h = Horario() #Se crea un Horario.
					h.profesional = ps[randrange(1, len(ps))] #Se le asigna un Profesional.
					h.hora_desde = self.horarios[horario] #Se le asigna una hora desde.
					h.hora_hasta = self.horarios[horario+1] #Se le asigna una hora hasta.
					h.dia_semana = dia #Se le asigna un dia de la semana.
					h.calendario = c #Se le asigna el calendario.
					h.save() #Y se guarda.
					
					#Comprobamos que el Horario generado no exista en el Calendario.
					existe = False
					for dh in c.horarios:
						for hh in dh:
							if h == hh:
								existe = True
					
					#Si ya existe continuamos generando.
					if existe:
						continue
					
					#Sino lo guardamos.
					h.save()
					
					#Y lo agregamos a la lista de horarios del Calendario
					c.agregar_horario(h)
		
	
	def evolucionar(self, ):
		pass
	
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
		
		for c in self.poblacion: #Por cada individuo en la poblacion.
			
			#Si el individuo ya fue evaluado seguimos con otro.
			if c.puntaje != 0:
				continue
			
			#Comparamos los horarios de las restriccines con las restriccinones de
			#los profesionales. Cada superposicion vale un punto, mientras mas
			#alto sea el puntaje, menos apto es el individuo. FALTA COMPROBAR QUE SEAN DEL MISMO DIA!!!
			for dia in c.horarios: #Por cada lista de dias.
				for h in dia: #Por cada horario en el dia.
					for r in self.restriccines: #Por cada restriccion.
						if (h.desde >= r.desde and h.desde <= r.hasta) or \
							(h.hasta >= r.desde and h.hasta <= r.hasta) or \
							(h.desde <= r.desde and h.hasta >= r.hasta):#OJOOOOOOO h.desde <= r.desde???
							c.puntaje += 1
						
		#Obtenemos todas las especialidades de la BBDD.
		es = Especialidad.objects.all()
		
		for c in self.poblacion: #Por cada individuo en la poblacion.
			
			for e in es: #Por cada especialidad
				
				horas_semanales = 0 #Contador de horas semanales.
				for dia in c.horarios: #Por cada lista de dias.
					for h in dia: #Por cada horario en el dia.
						
						#Si la especialidad del profes
						if h.profesional.especialidad == e:
							horas_semanales += 1
					
					if horas_semanales != e.carga_horaria_semanal:
						#-20% (del ranking)
						x = abs(e.carga_semanal - contador)
						#HARDCODED
						y = (35 - e.carga_semanal) / (x * 100)
						#HARDCODED
						p_total += (100 / len(especialidad) / (20 + y) * 100)
		
	
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
	
	@property
	def horarios(self, ):
		return self._horarios
	
	@horarios.setter
	def horarios(self, horarios):
		self._horarios = horarios
	
	@property
	def dias_habiles(self, ):
		return self._dias_habiles
	
	@dias_habiles.setter
	def dias_habiles(self, dias_habiles):
		self._dias_habiles = dias_habiles
	
